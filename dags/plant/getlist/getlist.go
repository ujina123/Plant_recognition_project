// JngMkk
package getlist

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

type PlantList struct {
	PlCode string
	PlName string
}

type Response struct {
	XMLName xml.Name `xml:"response"`
	Text    string   `xml:",chardata"`
	Header  struct {
		Text             string `xml:",chardata"`
		ResultCode       string `xml:"resultCode"`
		ResultMsg        string `xml:"resultMsg"`
		RequestParameter string `xml:"requestParameter"`
	} `xml:"header"`
	Body struct {
		Text  string `xml:",chardata"`
		Items struct {
			Text string `xml:",chardata"`
			Item []struct {
				Text            string `xml:",chardata"`
				CntntsNo        string `xml:"cntntsNo"`
				CntntsSj        string `xml:"cntntsSj"`
				RtnFileCours    string `xml:"rtnFileCours"`
				RtnFileSeCode   string `xml:"rtnFileSeCode"`
				RtnFileSn       string `xml:"rtnFileSn"`
				RtnImageDc      string `xml:"rtnImageDc"`
				RtnImgSeCode    string `xml:"rtnImgSeCode"`
				RtnOrginlFileNm string `xml:"rtnOrginlFileNm"`
				RtnStreFileNm   string `xml:"rtnStreFileNm"`
				RtnThumbFileNm  string `xml:"rtnThumbFileNm"`
			} `xml:"item"`
			NumOfRows  string `xml:"numOfRows"`
			PageNo     string `xml:"pageNo"`
			TotalCount string `xml:"totalCount"`
		} `xml:"items"`
	} `xml:"body"`
}

func ReplaceString(s string) string {
	return strings.ReplaceAll(s, "'", "")
}

func TrimSpace(s string) string {
	re := regexp.MustCompile(`\s{2,}`)
	return re.ReplaceAllString(s, "")
}

func GetPlantListChan(i int, r Response, c chan<- []PlantList) {
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
	var result Response
	var plants []PlantList
	c := make(chan []PlantList)
	gardenListURL := fmt.Sprintf("http://api.nongsaro.go.kr/service/garden/gardenList?apiKey=%s&pageNo=1&numOfRows=100", key)

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

	headers := []string{"plantCode", "plantName"}
	wErr := w.Write(headers)
	check.CheckErr(wErr)

	for _, v := range p {
		s := []string{v.PlCode, v.PlName}
		err := w.Write(s)
		check.CheckErr(err)
	}
}
