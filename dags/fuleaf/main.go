// JngMkk fuleaf crawling
package main

import (
	"encoding/csv"
	"log"
	"net/http"
	"os"
	"regexp"
	"strings"

	"github.com/PuerkitoBio/goquery"
)

type plants struct {
	name         string
	botanyNm     string
	info         string
	waterCycle   string
	waterInfo    string
	waterExp     string
	waterExpInfo string
	light        string
	lightInfo    string
	lightExp     string
	lightExpInfo string
	humidity     string
	humidInfo    string
	humidExp     string
	humidExpInfo string
	tempExp      string
	tempExpInfo  string
}

// newline 삭제
func trimSpaceNewlineInString(s string) string {
	re := regexp.MustCompile(`\n+`)
	return re.ReplaceAllString(s, " ")
}

// count -> detail
func replaceHref(s string) string {
	return strings.ReplaceAll(s, "count", "detail")
}

// : 기준 오른쪽 string
func splitC(s string) string {
	return strings.TrimSpace(strings.Split(s, ":")[1])
}

// 양 옆 공백 삭제
func trim(s string) string {
	return strings.TrimSpace(s)
}

// strings.Split -> split
func split(s, sep string) []string {
	return strings.Split(s, sep)
}

// strings.Contains -> contains
func contains(s, sep string) bool {
	return strings.Contains(s, sep)
}

// - 삭제
func deleteMinus(s string) string {
	return strings.ReplaceAll(s, "-", "")
}

// [~~~] 구문 삭제
func deleteString(s string) string {
	re := regexp.MustCompile(`\[[^)]*\]`)
	return re.ReplaceAllString(s, "")
}

// 공백 두 개 이상 삭제
func trimSpace(s string) string {
	re := regexp.MustCompile(`\s{2,}`)
	return re.ReplaceAllString(s, " ")
}

// 관리 제품 뒤로 제외
func containString(s string) string {
	var result string
	if contains(s, "[관리 제품]") {
		result = split(s, "[관리 제품]")[0]
	} else if contains(s, "[관리제품]") {
		result = split(s, "[관리제품]")[0]
	} else {
		result = s
	}
	return result
}

// check error
func checkErr(err error) {
	if err != nil {
		log.Fatalln(err)
	}
}

// check statuscode
func checkCode(res *http.Response) {
	if res.StatusCode != 200 {
		log.Fatalln("Request failed with Status:", res.StatusCode)
	}
}

// total page counts
func getHrefs() []string {
	var hrefs []string
	res, err := http.Get("https://fuleaf.com/plants")
	checkErr(err)
	checkCode(res)

	defer res.Body.Close()

	doc, err := goquery.NewDocumentFromReader(res.Body)
	checkErr(err)

	doc.Find(".plants__list-item").Each(func(i int, s *goquery.Selection) {
		h, _ := s.Find("a").Attr("href")
		url := "https://fuleaf.com" + replaceHref(h)
		hrefs = append(hrefs, url)
	})
	return hrefs
}

// info 크롤링
func getInfo(s *goquery.Selection, c chan<- plants) {
	nm := s.Find(".simpleinfo-plantname_korean.mainTitle").Text()
	inf := trimSpace(trim(trimSpaceNewlineInString(s.Find(".simpleinfo-plantname_intro").Text())))
	wCycle := trim(s.Find(".simpleinfo-table > ul > div:nth-child(1) > li:nth-child(1) > h1").Text())
	wInfo := trimSpace(trim(s.Find(".simpleinfo-table > ul > div:nth-child(1) > li:nth-child(1) > h2").Text()))
	lgt := trim(s.Find(".simpleinfo-table > ul > div:nth-child(1) > li:nth-child(2) > h1").Text())
	lInfo := trim(s.Find(".simpleinfo-table > ul > div:nth-child(1) > li:nth-child(2) > h2").Text())
	hd := trim(s.Find(".simpleinfo-table > ul > div:nth-child(2) > li:nth-child(1) > h1").Text())
	hdInfo := trim(s.Find(".simpleinfo-table > ul > div:nth-child(2) > li:nth-child(1) > h2").Text())
	boName := trim(s.Find(".simpleinfo-table > ul > div:nth-child(2) > li:nth-child(2) > h2").Text())
	lExp := trim(splitC(s.Find(".plants-raise-section > ul > li:nth-child(1) > h1").Text()))
	tExp := trim(splitC(s.Find(".plants-raise-section > ul > li:nth-child(2) > h1").Text()))
	hExp := trim(splitC(s.Find(".plants-raise-section > ul > li:nth-child(3) > h1").Text()))
	wExp := trim(splitC(s.Find(".plants-raise-section > ul > li:nth-child(4) > h1").Text()))

	lExpStr := s.Find(".plants-raise-section > ul > li:nth-child(1) > h2").Text()
	lExpStr = strings.Join(strings.Fields(lExpStr), " ")
	lExpInfo := trimSpace(trim(deleteMinus(deleteString(containString(lExpStr)))))

	tExpInfo := trimSpace(trim(deleteString(strings.Join(strings.Fields(s.Find(".plants-raise-section > ul > li:nth-child(2) > h2").Text()), " "))))

	hExpStr := s.Find(".plants-raise-section > ul > li:nth-child(3) > h2").Text()
	hExpStr = strings.Join(strings.Fields(hExpStr), " ")
	hExpInfo := trimSpace(trim(deleteMinus(deleteString(containString(hExpStr)))))

	wExpStr := s.Find(".plants-raise-section > ul > li:nth-child(4) > h2").Text()
	wExpStr = strings.Join(strings.Fields(wExpStr), " ")
	wExpInfo := trimSpace(trim(deleteMinus(deleteString(containString(wExpStr)))))

	c <- plants{
		name:         nm,
		info:         inf,
		waterCycle:   wCycle,
		waterInfo:    wInfo,
		light:        lgt,
		lightInfo:    lInfo,
		humidity:     hd,
		humidInfo:    hdInfo,
		botanyNm:     boName,
		lightExp:     lExp,
		lightExpInfo: lExpInfo,
		tempExp:      tExp,
		tempExpInfo:  tExpInfo,
		humidExp:     hExp,
		humidExpInfo: hExpInfo,
		waterExp:     wExp,
		waterExpInfo: wExpInfo,
	}
}

// 채널 받아주기
func getTotalInfo(href string, mainC chan<- []plants) {
	var pls []plants
	c := make(chan plants)

	res, err := http.Get(href)
	checkErr(err)
	checkCode(res)

	defer res.Body.Close()

	doc, err := goquery.NewDocumentFromReader(res.Body)
	checkErr(err)

	body := doc.Find("#plantDetail__page")
	body.Each(func(i int, s *goquery.Selection) {
		go getInfo(s, c)
	})

	for i := 0; i < body.Length(); i++ {
		pl := <-c
		pls = append(pls, pl)
	}

	mainC <- pls
}

// csv 파일 만들기
func writeCsv(p []plants) {
	file, err := os.Create("/home/ubuntu/finalproject/dags/data/fuleaf.csv")
	checkErr(err)

	w := csv.NewWriter(file)

	defer w.Flush()

	headers := []string{"name", "botanyNm", "info",
		"waterCycle", "waterInfo", "waterExp", "waterExpInfo",
		"light", "lightInfo", "lightExp", "lightExpInfo",
		"humidity", "humidInfo", "humidExp", "humidExpInfo",
		"tempExp", "tempExpInfo"}
	wErr := w.Write(headers)
	checkErr(wErr)

	for _, v := range p {
		slice := []string{v.name, v.botanyNm, v.info,
			v.waterCycle, v.waterInfo, v.waterExp, v.waterExpInfo,
			v.light, v.lightInfo, v.lightExp, v.lightExpInfo,
			v.humidity, v.humidInfo, v.humidExp, v.humidExpInfo,
			v.tempExp, v.tempExpInfo}
		jwErr := w.Write(slice)
		checkErr(jwErr)
	}
}

func main() {
	var pls []plants
	hrefs := getHrefs()
	c := make(chan []plants)

	for _, v := range hrefs {
		go getTotalInfo(v, c)
	}

	for i := 0; i < len(hrefs); i++ {
		pl := <-c
		pls = append(pls, pl...)
	}
	writeCsv(pls)
}
