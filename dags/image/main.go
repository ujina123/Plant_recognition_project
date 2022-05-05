package main

import (
	"log"
	"strings"
	"time"

	"github.com/PuerkitoBio/goquery"
	"github.com/fedesog/webdriver"
	"golang.org/x/net/html"
)

func checkErr(err error) {
	if err != nil {
		log.Fatalln(err)
	}
}

func sleep(x int) {
	time.Sleep(time.Duration(x) * time.Second)
}

func scroll(s *webdriver.Session) {
	lastPageHeight, err := s.ExecuteScript("return document.documentElement.scrollHeight", []interface{}{})
	checkErr(err)
	for {
		_, err := s.ExecuteScript("window.scrollTo(0, document.documentElement.scrollHeight)", []interface{}{})
		checkErr(err)
		sleep(3)
		newPageHeight, err := s.ExecuteScript("return document.documentElement.scrollHeight", []interface{}{})
		checkErr(err)
		if string(newPageHeight) == string(lastPageHeight) {
			break
		}
		lastPageHeight = newPageHeight
	}
}

func stringInSrcs(src string, srcs []string) bool {
	for _, val := range srcs {
		if val == src {
			return true
		}
	}
	return false
}

func googleSearch(s *goquery.Selection, srcs []string) []string {
	src, b := s.Find("img").Attr("src")
	if b {
		if !(stringInSrcs(src, srcs)) {
			srcs = append(srcs, src)
		}
	} else {
		src, _ = s.Find("img").Attr("data-src")
		if !(stringInSrcs(src, srcs)) {
			srcs = append(srcs, src)
		}
	}
	return srcs
}

func webSearch(s *goquery.Selection, srcs []string) []string {
	src, _ := s.Find("img").Attr("src")
	if !(stringInSrcs(src, srcs)) {
		srcs = append(srcs, src)
	}
	return srcs
}

func naverClick(s *webdriver.Session) {
	element, err := s.FindElement(webdriver.CSS_Selector, "ul.base > li:nth-child(2)")
	checkErr(err)
	textElement, err := element.FindElement(webdriver.CSS_Selector, "a")
	checkErr(err)
	text, err := textElement.Text()
	checkErr(err)
	if text == "이미지" {
		err := element.Click()
		checkErr(err)
	} else {
		element, err := s.FindElement(webdriver.CSS_Selector, "ul.base > li:nth-child(3)")
		checkErr(err)
		err2 := element.Click()
		checkErr(err2)
	}
}

func main() {
	var srcs []string
	driver := webdriver.NewChromeDriver("./chromedriver")
	err := driver.Start()
	checkErr(err)

	desired := webdriver.Capabilities{"Platform": "Linux"}
	required := webdriver.Capabilities{}

	session, err := driver.NewSession(desired, required)
	checkErr(err)

	// url := []string{"https://www.google.com/search?q=", "https://www.bing.com/images/search?q=", "https://search.naver.com/search.naver?where=nexearch&ie=utf8&query="}
	url := "https://www.google.com/search?q=" + "홍콩야자"
	openErr := session.Url(url)
	checkErr(openErr)
	sleep(3)

	goImg, err := session.FindElement(webdriver.CSS_Selector, "#hdtb-msb > div:nth-child(1) > div > div:nth-child(2) > a")
	checkErr(err)

	clickErr := goImg.Click()
	checkErr(clickErr)
	sleep(3)

	for {
		scroll(session)
		input, err := session.FindElement(webdriver.ClassName, "mye4qd")
		checkErr(err)
		clickErr := input.Click()
		if clickErr != nil {
			break
		}
	}

	res, err := session.Source()
	checkErr(err)

	html, err := html.Parse(strings.NewReader(res))
	checkErr(err)

	doc := goquery.NewDocumentFromNode(html)
	doc.Find("div.bRMDJf.islir").Each(func(i int, s *goquery.Selection) {
		srcs = googleSearch(s, srcs)
	})

	defer session.Delete()
	defer driver.Stop()
}
