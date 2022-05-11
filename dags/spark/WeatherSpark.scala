// JngMkk
import java.util.Properties
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions.Window

object WeatherSpark {
    def main(args: Array[String]) {
        val spark = SparkSession.builder.master("yarn").appName("weather").getOrCreate()
        
        var weather = spark.read.option("header", "true").csv("/home/data/weather.csv").select(col("areaNo").cast("long"),
                                                                                                to_timestamp(col("time")) as "time",
                                                                                                col("condiCode").cast("integer"),
                                                                                                col("isDay").cast("integer"),
                                                                                                col("temp").cast("integer"),
                                                                                                col("humidity").cast("integer"),
                                                                                                col("humidInfo"),
                                                                                                col("rainRatio").cast("integer"),
                                                                                                col("snowRatio").cast("integer"),
                                                                                                col("uv").cast("integer"),
                                                                                                col("uvInfo"))

        val region = spark.read.option("header", "true").csv("/home/data/region.csv")
        val condiCode = spark.read.option("header", "true").csv("/home/data/condiCode.csv").select(col("code"), col("title") as "condi")
        
        val rownum = row_number().over(Window.partitionBy(col("areaNo")).orderBy(col("time")))
        
        weather = weather.join(region, Seq("areaNo")).select(col("areaNo"),
                                                        col("si"), col("time"), rownum - 1 as "timeRank", 
                                                        col("condiCode") as "code", col("isDay"),
                                                        col("temp"), col("humidity"), col("humidInfo"), col("rainRatio"),
                                                        col("snowRatio"), col("uv"), col("uvInfo")).where(col("timeRank") < 24)
        
        weather = weather.join(condiCode, Seq("code")).select("areaNo", "si", "time", "timeRank", "condi", "isDay", "temp", "humidity", "humidInfo", "rainRatio", "snowRatio", "uv", "uvInfo")

        val window = Window.orderBy(col("areaNo"), col("timeRank"))

        weather = weather.withColumn("weatherId", row_number().over(window))
        
        weather = weather.select(col("weatherId"), col("areaNo"), col("si"), substring(date_format(col("time"), "yyyyMMddHHmm").cast("string"), 9, 2).cast("integer") as "time", col("condi"), col("isDay"), col("temp"), col("humidity"), col("humidInfo"), col("rainRatio"), col("snowRatio"), col("uv"), col("uvInfo"))
        
        val prop = new Properties()
        prop.put("driver", "com.mysql.cj.jdbc.Driver")
        prop.put("user", "root")
        prop.put("password", "1234")
        
        weather.write.mode("overwrite").option("truncate", "true").jdbc("jdbc:mysql://localhost:3306/finalproject", "weather", prop)
    }
}
