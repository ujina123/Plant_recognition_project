// JngMkk
package dryplant

import "encoding/xml"

type DryPlantList struct {
	DryPlCode string
	DryPlName string
}

type ListRes struct {
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
				Text         string `xml:",chardata"`
				ClNm         string `xml:"clNm"`
				CntntsNo     string `xml:"cntntsNo"`
				CntntsSj     string `xml:"cntntsSj"`
				ImgUrl1      string `xml:"imgUrl1"`
				ImgUrl2      string `xml:"imgUrl2"`
				Scnm         string `xml:"scnm"`
				ThumbImgUrl1 string `xml:"thumbImgUrl1"`
				ThumbImgUrl2 string `xml:"thumbImgUrl2"`
			} `xml:"item"`
			NumOfRows  string `xml:"numOfRows"`
			PageNo     string `xml:"pageNo"`
			TotalCount string `xml:"totalCount"`
		} `xml:"items"`
	} `xml:"body"`
}
