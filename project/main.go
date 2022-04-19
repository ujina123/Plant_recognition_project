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

	"github.com/JngMkk/project/weather"

	"github.com/JngMkk/project/check"
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
	humidity := strconv.Itoa(result.Current.Humidity)
	uv := strconv.Itoa(int(result.Current.Uv))
	var rainRatio string
	var snowRatio string
	w = weather.Weather{
		AreaNo:    areaNo,
		Time:      current,
		CondiCode: condiCode,
		IsDay:     isDay,
		Temp:      temp,
		Humidity:  humidity,
		RainRatio: rainRatio,
		SnowRatio: snowRatio,
		Uv:        uv,
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
			uv = strconv.Itoa(int(v.Uv))
			w = weather.Weather{
				AreaNo:    areaNo,
				Time:      wtime,
				CondiCode: condiCode,
				IsDay:     isDay,
				Temp:      temp,
				Humidity:  humidity,
				RainRatio: rainRatio,
				SnowRatio: snowRatio,
				Uv:        uv,
			}
			weathers = append(weathers, w)
		}
	}
	weathers = checkWeatherCode(weathers)
	c <- weathers
}

func writeCsv(weathers []weather.Weather) {
	file, err := os.Create("/home/ubuntu/go/src/github.com/JngMkk/project/data/weather.csv")
	check.CheckError(err)

	w := csv.NewWriter(file)

	defer w.Flush()

	headers := []string{"areaNo", "time", "condiCode", "isDay", "temp", "humidity", "rainRatio", "snowRatio", "uv"}
	wErr := w.Write(headers)
	check.CheckError(wErr)

	for _, wea := range weathers {
		s := []string{wea.AreaNo, wea.Time, wea.CondiCode, wea.IsDay, wea.Temp, wea.Humidity, wea.RainRatio, wea.SnowRatio, wea.Uv}
		err := w.Write(s)
		check.CheckError(err)
	}
}

func main() {
	region := weather.GetRegion("/home/ubuntu/go/src/github.com/JngMkk/project/data/region.csv")
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
