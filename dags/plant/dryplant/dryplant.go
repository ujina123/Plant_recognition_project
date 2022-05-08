// JngMkk
package dryplant

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
	"github.com/JngMkk/plant/plantinfo"
)

func ReplaceSok(s string) string {
	return strings.ReplaceAll(s, "속", "")
}

func ReplaceA(s string) string {
	re := regexp.MustCompile(`[‘|’]`)
	return re.ReplaceAllString(s, "")
}

func ReplaceGGuksae(s string) string {
	return strings.ReplaceAll(s, "<br />", " ")
}

func GetDryListChan(i int, r ListRes, c chan<- []DryPlantList) {
	var dryP DryPlantList
	var dryPs []DryPlantList

	list := r.Body.Items.Item
	dryPCls := ReplaceSok(plantinfo.DeleteString(list[i].ClNm))
	dryPCode := list[i].CntntsNo
	dryPName := plantinfo.DeleteString(plantinfo.ReplaceString(ReplaceA(list[i].CntntsSj)))
	dryPNameList := strings.Split(dryPName, " ")
	if len(dryPNameList) == 1 {
		dryPName = dryPCls + dryPName
	}
	dryP = DryPlantList{
		DryPlCode: dryPCode,
		DryPlName: dryPName,
	}
	dryPs = append(dryPs, dryP)
	c <- dryPs
}

func GetDryList(key string) []DryPlantList {
	var result ListRes
	var dPlants []DryPlantList
	c := make(chan []DryPlantList)
	url := fmt.Sprintf("http://api.nongsaro.go.kr/service/dryGarden/dryGardenList?apiKey=%s&numOfRows=1000", key)

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

	list := result.Body.Items.Item
	for i := 0; i < len(list); i++ {
		go GetDryListChan(i, result, c)
	}

	for i := 0; i < len(list); i++ {
		dPlants = append(dPlants, <-c...)
	}
	return dPlants
}

func GetInfoStruct(r InfoRes, c chan<- DryPlInfo) {
	dryPlCode := r.Body.Item.CntntsNo
	clsInfo := ReplaceGGuksae(plantinfo.TrimSpaceNewlineInString(r.Body.Item.ClCodeDc))
	flInfo := ReplaceGGuksae(r.Body.Item.FlwrInfo)
	light := ReplaceGGuksae(r.Body.Item.LighttInfo)
	place := ReplaceGGuksae(plantinfo.TrimSpaceNewlineInString(r.Body.Item.BatchPlaceInfo))
	manageLevel := r.Body.Item.ManageLevelNm
	growInfo := ReplaceGGuksae(r.Body.Item.GrwtInfo)
	growSpeed := r.Body.Item.GrwtseVeNm
	growTemp := r.Body.Item.GrwhTpInfo
	winterTemp := r.Body.Item.PswntrTpInfo
	water := ReplaceGGuksae(plantinfo.TrimSpaceNewlineInString(r.Body.Item.WaterCycleInfo))
	highTempHd := r.Body.Item.HgtmMhmrInfo
	character := ReplaceGGuksae(plantinfo.TrimSpaceNewlineInString(r.Body.Item.ChartrInfo))

	c <- DryPlInfo{
		DryPlCode:   dryPlCode,
		ClsInfo:     clsInfo,
		FlInfo:      flInfo,
		Light:       light,
		Place:       place,
		ManageLevel: manageLevel,
		GrowInfo:    growInfo,
		GrowSpeed:   growSpeed,
		GrowTemp:    growTemp,
		WinterTemp:  winterTemp,
		Water:       water,
		HighTempHd:  highTempHd,
		Character:   character,
	}
}

func GetDryInfo(key string, list []DryPlantList) []DryPlInfo {
	var result InfoRes
	var dryInfos []DryPlInfo
	c := make(chan DryPlInfo)

	for _, v := range list {
		url := fmt.Sprintf("http://api.nongsaro.go.kr/service/dryGarden/dryGardenDtl?apiKey=%s&cntntsNo=%s&numOfRows=100", key, v.DryPlCode)
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

	for i := 0; i < len(list); i++ {
		dryPl := <-c
		dryInfos = append(dryInfos, dryPl)
	}
	return dryInfos
}

func DryPlListToCsv(p []DryPlantList) {
	file, err := os.Create("/home/ubuntu/finalproject/dags/data/dryPlantList.csv")
	check.CheckErr(err)

	w := csv.NewWriter(file)

	defer w.Flush()

	headers := []string{"dryPlCode", "dryPlName"}
	wErr := w.Write(headers)
	check.CheckErr(wErr)

	for _, v := range p {
		s := []string{v.DryPlCode, v.DryPlName}
		err := w.Write(s)
		check.CheckErr(err)
	}
}

func DryPlInfoToCsv(key string) {
	file, err := os.Create("/home/ubuntu/finalproject/dags/data/dryPlantInfo.csv")
	check.CheckErr(err)

	w := csv.NewWriter(file)

	defer w.Flush()

	headers := []string{"dryPlCode", "clsInfo", "flInfo", "light", "place", "manageLevel",
		"growInfo", "growSpeed", "growTemp", "winterTemp", "water", "highTempHd", "character"}
	wErr := w.Write(headers)
	check.CheckErr(wErr)

	dryList := GetDryList(key)
	dryInfo := GetDryInfo(key, dryList)

	DryPlListToCsv(dryList)

	for _, d := range dryInfo {
		s := []string{d.DryPlCode, d.ClsInfo, d.FlInfo, d.Light, d.Place, d.ManageLevel,
			d.GrowInfo, d.GrowSpeed, d.GrowTemp, d.WinterTemp, d.Water, d.HighTempHd, d.Character}
		err := w.Write(s)
		check.CheckErr(err)
	}
}
