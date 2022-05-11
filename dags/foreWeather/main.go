//JngMkk forecast weather
package main

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"net/http"
	"os"
	"strconv"
	"time"

	"github.com/JngMkk/foreWeather/weather"

	"github.com/JngMkk/foreWeather/check"
)

func checkWeatherCode(wea []weather.Weather) []weather.Weather {
	for i, w := range wea {
		if weather.StringInRain(w.CondiCode, []string{"1063", "1180", "1183", "1186", "1189", "1192", "1195", "1246"}) {
			wea[i].CondiCode = "1015"
			continue
		} else if weather.StringInSmallRain(w.CondiCode, []string{"1072", "1150", "1153", "1168", "1171"}) {
			wea[i].CondiCode = "1018"
			continue
		} else if weather.StringInSmog(w.CondiCode, []string{"1135", "1147"}) {
			wea[i].CondiCode = "1030"
			continue
		} else if weather.StringInStrongRain(w.CondiCode, []string{"1240", "1243"}) {
			wea[i].CondiCode = "1027"
			continue
		} else if weather.StringInThunderRain(w.CondiCode, []string{"1273", "1276"}) {
			wea[i].CondiCode = "1036"
			continue
		} else if weather.StringInThunder(w.CondiCode, []string{"1087"}) {
			wea[i].CondiCode = "1021"
			continue
		} else if weather.StringInSnow(w.CondiCode, []string{"1066", "1069", "1114", "1117", "1204", "1207", "1210", "1213", "1216", "1219", "1222", "1225", "1249", "1252", "1255", "1258"}) {
			wea[i].CondiCode = "1012"
			continue
		} else if weather.StringInIcePallet(w.CondiCode, []string{"1198", "1201", "1237", "1261", "1264"}) {
			wea[i].CondiCode = "1024"
			continue
		} else if weather.StringInThunderSnow(w.CondiCode, []string{"1279", "1282"}) {
			wea[i].CondiCode = "1033"
			continue
		} else {
			continue
		}
	}
	return wea
}

func getWeather(lat, lng, aN string, c chan<- []weather.Weather) {
	var weathers []weather.Weather
	var w weather.Weather
	var uvinfo, humidinfo string
	res, err := http.Get(fmt.Sprintf("http://api.weatherapi.com/v1/forecast.json?key=&q=%s,%s&days=2", lat, lng))
	check.CheckError(err)
	check.CheckCode(res)
	defer res.Body.Close()
	body, err := ioutil.ReadAll(res.Body)
	check.CheckError(err)
	var result weather.Response
	if err := json.Unmarshal(body, &result); err != nil {
		log.Fatalln(err)
	}
	areaNo := aN
	current := time.Now().Format("2006-01-02 15:04")
	condiCode := strconv.Itoa(result.Current.Condition.Code)
	isDay := strconv.Itoa(result.Current.IsDay)
	temp := strconv.Itoa(int(math.Round(result.Current.TempC)))
	humidInt := result.Current.Humidity
	humidity := strconv.Itoa(humidInt)
	uvInt := int(result.Current.Uv)
	uv := strconv.Itoa(uvInt)
	if uvInt < 3 {
		uvinfo = fmt.Sprintf("자외선 지수는 %d로 낮은 수준입니다. 식물들이 좋아하겠네요!", uvInt)
	} else if uvInt < 6 {
		uvinfo = fmt.Sprintf("자외선 지수는 %d로 보통 수준입니다. 식물들이 좋아하겠네요!", uvInt)
	} else if uvInt < 8 {
		uvinfo = fmt.Sprintf("자외선 지수는 %d로 높은 수준입니다. 식물들도 자외선에 약하니 주의해주세요.", uvInt)
	} else if uvInt < 11 {
		uvinfo = fmt.Sprintf("자외선 지수는 %d로 매우 높은 수준입니다. 식물들을 실내로 옮겨주세요!", uvInt)
	} else {
		uvinfo = fmt.Sprintf("자외선 지수는 %d로 위험한 수준입니다. 식물들이 햇빛의 직사광선에 맞지 않게 해주세요!", uvInt)
	}
	if humidInt < 40 {
		humidinfo = "현재 습도는 " + strconv.Itoa(humidInt) + "%로 건조한 날씨입니다. 건조에 약한 식물을 잘 보살펴 주세요."
	} else if humidInt > 70 {
		humidinfo = "현재 습도는 " + strconv.Itoa(humidInt) + "%로 매우 습한 날씨입니다. 습한 환경에 약한 식물을 잘 보살펴 주세요."
	} else {
		humidinfo = "현재 습도는 " + strconv.Itoa(humidInt) + "%로 쾌적한 날씨입니다. 식물을 키우기 딱 좋아요!"
	}
	var rainRatio string
	var snowRatio string
	w = weather.Weather{
		AreaNo:    areaNo,
		Time:      current,
		CondiCode: condiCode,
		IsDay:     isDay,
		Temp:      temp,
		Humidity:  humidity,
		HumidInfo: humidinfo,
		RainRatio: rainRatio,
		SnowRatio: snowRatio,
		Uv:        uv,
		UvInfo:    uvinfo,
	}
	weathers = append(weathers, w)
	for i := 0; i < len(result.Forecast.Forecastday); i++ {
		fore := result.Forecast.Forecastday[i].Hour
		for _, v := range fore {
			wtime := v.Time
			date, err := time.Parse("2006-01-02 15:04", wtime)
			check.CheckError(err)
			dateNow, err := time.Parse("2006-01-02 15:04", current)
			check.CheckError(err)
			if date.Before(dateNow) {
				continue
			}
			condiCode = strconv.Itoa(v.Condition.Code)
			isDay = strconv.Itoa(v.IsDay)
			temp = strconv.Itoa(int(math.Round(v.TempC)))
			humidity = strconv.Itoa(v.Humidity)
			rainRatio = strconv.Itoa(int(math.Round(v.ChanceOfRain)))
			snowRatio = strconv.Itoa(int(math.Round(v.ChanceOfSnow)))
			uvInt = int(v.Uv)
			uv = strconv.Itoa(uvInt)
			if uvInt < 3 {
				uvinfo = fmt.Sprintf("자외선 지수는 %d로 낮은 수준입니다. 식물들이 좋아하겠네요!", uvInt)
			} else if uvInt < 6 {
				uvinfo = fmt.Sprintf("자외선 지수는 %d로 보통 수준입니다. 식물들이 좋아하겠네요!", uvInt)
			} else if uvInt < 8 {
				uvinfo = fmt.Sprintf("자외선 지수는 %d로 높은 수준입니다. 식물들도 자외선에 약하니 주의해주세요.", uvInt)
			} else if uvInt < 11 {
				uvinfo = fmt.Sprintf("자외선 지수는 %d로 매우 높은 수준입니다. 식물들이 다치지 않도록 유의해주세요!", uvInt)
			} else {
				uvinfo = fmt.Sprintf("자외선 지수는 %d로 위험한 수준입니다. 식물들을 실내로 옮겨주세요!", uvInt)
			}
			w = weather.Weather{
				AreaNo:    areaNo,
				Time:      wtime,
				CondiCode: condiCode,
				IsDay:     isDay,
				Temp:      temp,
				Humidity:  humidity,
				HumidInfo: "",
				RainRatio: rainRatio,
				SnowRatio: snowRatio,
				Uv:        uv,
				UvInfo:    uvinfo,
			}
			weathers = append(weathers, w)
		}
	}
	weathers = checkWeatherCode(weathers)
	c <- weathers
}

func writeCsv(weathers []weather.Weather) {
	file, err := os.Create("/home/ubuntu/finalproject/dags/data/weather.csv")
	check.CheckError(err)

	w := csv.NewWriter(file)

	defer w.Flush()

	headers := []string{"areaNo", "time", "condiCode", "isDay", "temp", "humidity", "humidInfo", "rainRatio", "snowRatio", "uv", "uvInfo"}
	wErr := w.Write(headers)
	check.CheckError(wErr)

	for _, wea := range weathers {
		s := []string{wea.AreaNo, wea.Time, wea.CondiCode, wea.IsDay, wea.Temp, wea.Humidity, wea.HumidInfo, wea.RainRatio, wea.SnowRatio, wea.Uv, wea.UvInfo}
		err := w.Write(s)
		check.CheckError(err)
	}
}

func main() {
	region := weather.GetRegion("/home/ubuntu/finalproject/dags/data/region.csv")
	c := make(chan []weather.Weather)
	var weathers []weather.Weather

	for i, v := range region {
		go getWeather(v[2], v[1], region[i][0], c)
	}

	for j := 0; j < len(region); j++ {
		weathers = append(weathers, <-c...)
	}

	writeCsv(weathers)
}
