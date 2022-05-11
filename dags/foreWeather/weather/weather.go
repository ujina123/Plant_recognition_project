// JngMkk
package weather

import (
	"encoding/csv"
	"os"

	"github.com/JngMkk/foreWeather/check"
)

type Weather struct {
	AreaNo    string
	Time      string
	CondiCode string
	IsDay     string
	Temp      string
	Humidity  string
	HumidInfo string
	RainRatio string
	SnowRatio string
	Uv        string
	UvInfo    string
}

type Response struct {
	Location struct {
		Name           string  `json:"name"`
		Region         string  `json:"region"`
		Country        string  `json:"country"`
		Lat            float64 `json:"lat"`
		Lon            float64 `json:"lon"`
		TzID           string  `json:"tz_id"`
		LocaltimeEpoch int     `json:"localtime_epoch"`
		Localtime      string  `json:"localtime"`
	} `json:"location"`
	Current struct {
		TempC     float64 `json:"temp_c"`
		IsDay     int     `json:"is_day"`
		Condition struct {
			Code int `json:"code"`
		} `json:"condition"`
		Humidity int     `json:"humidity"`
		Uv       float64 `json:"uv"`
	} `json:"current"`
	Forecast struct {
		Forecastday []struct {
			Date string `json:"date"`
			Day  struct {
				Condition struct {
				} `json:"condition"`
			} `json:"day"`
			Astro struct {
			} `json:"astro"`
			Hour []struct {
				Time      string  `json:"time"`
				TempC     float64 `json:"temp_c"`
				IsDay     int     `json:"is_day"`
				Condition struct {
					Code int `json:"code"`
				} `json:"condition"`
				Humidity     int     `json:"humidity"`
				ChanceOfRain float64 `json:"chance_of_rain"`
				ChanceOfSnow float64 `json:"chance_of_snow"`
				Uv           float64 `json:"uv"`
			} `json:"hour"`
		} `json:"forecastday"`
	} `json:"forecast"`
}

func AddItem(slice *[][]string, item ...string) {
	*slice = append(*slice, item)
}

func GetRegion(path string) [][]string {
	var rows [][]string
	csvFile, err := os.Open(path)
	check.CheckError(err)
	defer csvFile.Close()

	items, err := csv.NewReader(csvFile).ReadAll()
	check.CheckError(err)
	for i, item := range items {
		if i > 0 {
			areaNo := item[1]
			lng := item[6]
			lat := item[7]
			AddItem(&rows, areaNo, lng, lat)
		}
	}
	return rows
}

func StringInSnow(code string, list []string) bool {
	for _, val := range list {
		if val == code {
			return true
		}
	}
	return false
}

func StringInRain(code string, list []string) bool {
	for _, val := range list {
		if val == code {
			return true
		}
	}
	return false
}

func StringInSmallRain(code string, list []string) bool {
	for _, val := range list {
		if val == code {
			return true
		}
	}
	return false
}

func StringInThunder(code string, list []string) bool {
	for _, val := range list {
		if val == code {
			return true
		}
	}
	return false
}

func StringInIcePallet(code string, list []string) bool {
	for _, val := range list {
		if val == code {
			return true
		}
	}
	return false
}

func StringInStrongRain(code string, list []string) bool {
	for _, val := range list {
		if val == code {
			return true
		}
	}
	return false
}

func StringInSmog(code string, list []string) bool {
	for _, val := range list {
		if val == code {
			return true
		}
	}
	return false
}

func StringInThunderSnow(code string, list []string) bool {
	for _, val := range list {
		if val == code {
			return true
		}
	}
	return false
}

func StringInThunderRain(code string, list []string) bool {
	for _, val := range list {
		if val == code {
			return true
		}
	}
	return false
}
