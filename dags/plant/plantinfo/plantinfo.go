package plantinfo

import (
	"encoding/csv"
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"

	"github.com/JngMkk/plant/check"
)

func ReplaceString(s string) string {
	return strings.ReplaceAll(s, "'", "")
}

func TrimSpace(s string) string {
	re := regexp.MustCompile(`\s{2,}`)
	return re.ReplaceAllString(s, "")
}

func TrimSpaceNewlineInString(s string) string {
	re := regexp.MustCompile(`\n+`)
	return re.ReplaceAllString(s, " ")
}

func ReplaceI(s string) string {
	re := regexp.MustCompile(`[<i>|</i>]`)
	return re.ReplaceAllString(s, "")
}

func DeleteString(s string) string {
	re := regexp.MustCompile(`\([^)]*\)`)
	return re.ReplaceAllString(s, "")
}

func GetPlantListChan(i int, r ListRes, c chan<- []PlantList) {
	var plant PlantList
	var plants []PlantList
	list := r.Body.Items.Item
	plantCode := list[i].CntntsNo
	plantName := TrimSpace(ReplaceString(list[i].CntntsSj))
	plant = PlantList{
		PlCode: plantCode,
		PlName: plantName,
	}
	plants = append(plants, plant)
	c <- plants
}

func GetPlantList(key string) []PlantList {
	var result ListRes
	var plants []PlantList
	c := make(chan []PlantList)
	gardenListURL := fmt.Sprintf("http://api.nongsaro.go.kr/service/garden/gardenList?apiKey=%s&pageNo=1&numOfRows=1000", key)

	res, err := http.Get(gardenListURL)
	check.CheckErr(err)
	check.CheckRes(res)

	defer res.Body.Close()

	body, err := ioutil.ReadAll(res.Body)
	check.CheckErr(err)

	Xerr := xml.Unmarshal(body, &result)
	check.CheckErr(Xerr)

	if result.Header.ResultCode != "00" {
		log.Fatalln("API Error")
	}

	list := result.Body.Items.Item
	for i := 0; i < len(list); i++ {
		go GetPlantListChan(i, result, c)
	}

	for i := 0; i < len(list); i++ {
		plants = append(plants, <-c...)
	}

	return plants
}

func PlantListToCsv(p []PlantList) {
	file, err := os.Create("/home/ubuntu/finalproject/dags/data/plantList.csv")
	check.CheckErr(err)

	w := csv.NewWriter(file)

	defer w.Flush()

	headers := []string{"plCode", "plName"}
	wErr := w.Write(headers)
	check.CheckErr(wErr)

	for _, v := range p {
		s := []string{v.PlCode, v.PlName}
		err := w.Write(s)
		check.CheckErr(err)
	}
}

func GetInfoStruct(r InfoRes, c chan<- PlantInfo) {
	plCode := r.Body.Item.CntntsNo
	divName := r.Body.Item.ClCodeNm
	eclgyName := r.Body.Item.EclgyCodeNm
	height := r.Body.Item.GrowthHgInfo
	area := r.Body.Item.GrowthAraInfo
	flColor := r.Body.Item.FlclrCodeNm
	flSeason := r.Body.Item.IgnSeasonCodeNm
	smellCode := r.Body.Item.SmellCode
	lightDemand := r.Body.Item.LighttdemanddoCodeNm
	place := DeleteString(r.Body.Item.PostngplaceCodeNm)
	toxic := r.Body.Item.ToxctyInfo
	levelCode := r.Body.Item.ManagelevelCode
	growSpeedCode := r.Body.Item.GrwtveCode
	growTempCode := r.Body.Item.GrwhTpCode
	winterLowCode := r.Body.Item.WinterLwetTpCode
	humidityCode := r.Body.Item.HdCode
	springWtCode := r.Body.Item.WatercycleSprngCode
	summerWtCode := r.Body.Item.WatercycleSummerCode
	autumnWtCode := r.Body.Item.WatercycleAutumnCode
	winterWtCode := r.Body.Item.WatercycleWinterCode
	speclManage := TrimSpaceNewlineInString(r.Body.Item.SpeclmanageInfo) + " " + TrimSpaceNewlineInString(r.Body.Item.FncltyInfo)

	c <- PlantInfo{
		PlCode:        plCode,
		DivName:       divName,
		EclgyName:     eclgyName,
		Height:        height,
		Area:          area,
		FlColor:       flColor,
		FlSeason:      flSeason,
		SmellCode:     smellCode,
		LightDemand:   lightDemand,
		Place:         place,
		Toxic:         toxic,
		LevelCode:     levelCode,
		GrowSpeedCode: growSpeedCode,
		GrowTempCode:  growTempCode,
		WinterLowCode: winterLowCode,
		HumidityCode:  humidityCode,
		SpringWtCode:  springWtCode,
		SummerWtCode:  summerWtCode,
		AutumnWtCode:  autumnWtCode,
		WinterWtCode:  winterWtCode,
		SpeclManage:   speclManage,
	}
}

func GetInfo(key string, p []PlantList) []PlantInfo {
	var result InfoRes
	var plInfos []PlantInfo
	c := make(chan PlantInfo)

	for _, v := range p {
		url := fmt.Sprintf("http://api.nongsaro.go.kr/service/garden/gardenDtl?apiKey=%s&cntntsNo=%s&pageNo=1&numOfRows=100", key, v.PlCode)
		res, err := http.Get(url)
		check.CheckErr(err)
		check.CheckRes(res)

		defer res.Body.Close()
		body, err := ioutil.ReadAll(res.Body)
		check.CheckErr(err)
		Xerr := xml.Unmarshal(body, &result)
		check.CheckErr(Xerr)
		if result.Header.ResultCode != "00" {
			log.Fatalln("API Error")
		}
		go GetInfoStruct(result, c)
	}

	for i := 0; i < len(p); i++ {
		pl := <-c
		plInfos = append(plInfos, pl)
	}
	return plInfos
}

func makeSlice(v PlantInfo, mainC chan<- []string) {
	s := []string{v.PlCode, v.DivName, v.EclgyName, v.Height, v.Area, v.FlColor, v.FlSeason,
		v.SmellCode, v.LightDemand, v.Place, v.Toxic, v.LevelCode, v.GrowSpeedCode,
		v.GrowTempCode, v.WinterLowCode, v.HumidityCode,
		v.SpringWtCode, v.SummerWtCode, v.AutumnWtCode, v.WinterWtCode, v.SpeclManage}
	mainC <- s
}

func PlantInfoToCsv(key string) {
	c := make(chan []string)
	file, err := os.Create("/home/ubuntu/finalproject/dags/data/plantInfo.csv")
	check.CheckErr(err)

	w := csv.NewWriter(file)

	defer w.Flush()

	headers := []string{"plCode", "divName", "eclgyName", "height", "area", "flColor",
		"flSeason", "smellCode", "lightDemand", "place", "toxic", "levelCode", "growSpeedCode",
		"growTempCode", "winterLowCode", "humidityCode", "springWtCode", "summerWtCode",
		"autumnWtCode", "winterWtCode", "speclManage"}
	wErr := w.Write(headers)
	check.CheckErr(wErr)

	plList := GetPlantList(key)
	PlantListToCsv(plList)

	p := GetInfo(key, plList)

	for _, v := range p {
		go makeSlice(v, c)
	}
	for i := 0; i < len(p); i++ {
		err := w.Write(<-c)
		check.CheckErr(err)
	}
}
