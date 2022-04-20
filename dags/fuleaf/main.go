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
	name       string
	info       string
	waterCycle string
	waterInfo  string // 물 + info
	lightInfo  string
	humidity   string
}

func trimSpaceNewlineInString(s string) string {
	re := regexp.MustCompile(`\n+`)
	return re.ReplaceAllString(s, " ")
}

func replaceHref(s string) string {
	return strings.ReplaceAll(s, "count", "detail")
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

func getInfo(href string, c chan<- plants) {
	res, err := http.Get(href)
	checkErr(err)
	checkCode(res)

	defer res.Body.Close()

	doc, err := goquery.NewDocumentFromReader(res.Body)
	checkErr(err)

	nm := doc.Find(".simpleinfo-plantname_korean.mainTitle").Text()
	inf := trimSpaceNewlineInString(doc.Find(".simpleinfo-plantname_intro").Text())
	wCycle := doc.Find(".simpleinfo-table > ul > div:nth-child(1) > li:nth-child(1) > h1").Text()
	wInfo := doc.Find(".plants-raise-section > ul > li:nth-child(4) > h1").Text() + " " + doc.Find(".simpleinfo-table > ul > div:nth-child(1) > li:nth-child(1) > h2").Text()
	light := doc.Find(".simpleinfo-table > ul > div:nth-child(1) > li:nth-child(2) > h1").Text() + " " + doc.Find(".simpleinfo-table > ul > div:nth-child(1) > li:nth-child(2) > h2").Text()
	hd := doc.Find(".simpleinfo-table > ul > div:nth-child(2) > li:nth-child(1) > h1").Text()

	c <- plants{
		name:       nm,
		info:       inf,
		waterCycle: wCycle,
		waterInfo:  wInfo,
		lightInfo:  light,
		humidity:   hd,
	}
}

func getTotalInfo(hrefs []string) []plants {
	var pls []plants
	c := make(chan plants)

	for _, v := range hrefs {
		go getInfo(v, c)
	}

	for i := 0; i < len(hrefs); i++ {
		pl := <-c
		pls = append(pls, pl)
	}
	return pls
}

func writeCsv(p []plants) {
	file, err := os.Create("./data/fuleaf.csv")
	checkErr(err)

	w := csv.NewWriter(file)

	defer w.Flush()

	headers := []string{"name", "info", "waterCycle", "waterInfo", "lightInfo", "humidity"}
	wErr := w.Write(headers)
	checkErr(wErr)

	for _, v := range p {
		slice := []string{v.name, v.info, v.waterCycle, v.waterInfo, v.lightInfo, v.humidity}
		jwErr := w.Write(slice)
		checkErr(jwErr)
	}
}

func main() {
	hrefs := getHrefs()
	info := getTotalInfo(hrefs)
	writeCsv(info)
}
