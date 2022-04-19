// JngMkk
import java.util.Properties
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.expressions.Window

object WeatherSpark {
    def main(args: Array[String]) {
        val spark = SparkSession.builder.master("yarn").appName("weather").getOrCreate()
        
        var weather = spark.read.option("header", "true").csv("/home/data/weather.csv").select(col("areaNo").cast("long"),
                                                                                                to_timestamp(col("time"), "yyyy-MM-dd HH:mm") as "time",
                                                                                                col("condiCode").cast("integer"),
                                                                                                col("isDay").cast("integer"),
                                                                                                col("temp").cast("integer"),
                                                                                                col("humidity").cast("integer"),
                                                                                                col("rainRatio").cast("integer"),
                                                                                                col("snowRatio").cast("integer"),
                                                                                                col("uv").cast("integer"))

        val region = spark.read.option("header", "true").csv("/home/data/region.csv")
        val condiCode = spark.read.option("header", "true").csv("/home/data/condiCode.csv").select(col("code"), col("title") as "condi")
        
        val rownum = row_number().over(Window.partitionBy(col("areaNo")).orderBy(col("time")))
        
        weather = weather.join(region, Seq("areaNo")).select(col("areaNo"),
                                                        col("si"), rownum - 1 as "time", 
                                                        col("condiCode") as "code", col("isDay"), 
                                                        col("temp"), col("humidity"), col("rainRatio"),
                                                        col("snowRatio")).where(col("time") < 24)
        
        weather = weather.join(condiCode, Seq("code")).select("areaNo", "si", "time", "condi", "isDay", "temp", "humidity", "rainRatio", "snowRatio")
        
        val prop = new Properties()
        prop.put("driver", "com.mysql.cj.jdbc.Driver")
        prop.put("user", "root")
        prop.put("password", "1234")
        
        weather.orderBy("areaNo", "time").write.mode("overwrite").jdbc("jdbc:mysql://localhost:3306/finalproject", "weather", prop)
    }
}
