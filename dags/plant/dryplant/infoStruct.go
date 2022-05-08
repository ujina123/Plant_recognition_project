// JngMkk
package dryplant

import "encoding/xml"

type DryPlInfo struct {
	DryPlCode   string // 식물코드
	ClsInfo     string // 과 설명
	FlInfo      string // 꽃 정보
	Light       string // 광 정보
	Place       string // 위치
	ManageLevel string // 관리수준
	GrowInfo    string // 생장 정보
	GrowSpeed   string // 생장 속도
	GrowTemp    string // 생육 온도
	WinterTemp  string // 월동 온도
	Water       string // 물주기 정보
	HighTempHd  string // 고온다습
	Character   string // 특성
}

type InfoRes struct {
	XMLName xml.Name `xml:"response"`
	Text    string   `xml:",chardata"`
	Header  struct {
		Text             string `xml:",chardata"`
		ResultCode       string `xml:"resultCode"`
		ResultMsg        string `xml:"resultMsg"`
		RequestParameter struct {
			Text     string `xml:",chardata"`
			CntntsNo string `xml:"cntntsNo"`
		} `xml:"requestParameter"`
	} `xml:"header"`
	Body struct {
		Text string `xml:",chardata"`
		Item struct {
			Text           string `xml:",chardata"`
			BatchPlaceInfo string `xml:"batchPlaceInfo"`
			ChartrInfo     string `xml:"chartrInfo"`
			ClCodeDc       string `xml:"clCodeDc"`
			ClNm           string `xml:"clNm"`
			CntntsNo       string `xml:"cntntsNo"`
			CntntsSj       string `xml:"cntntsSj"`
			DistbNm        string `xml:"distbNm"`
			DlthtsInfo     string `xml:"dlthtsInfo"`
			FlwrInfo       string `xml:"flwrInfo"`
			FrtlzrInfo     string `xml:"frtlzrInfo"`
			GrwhTpInfo     string `xml:"grwhTpInfo"`
			GrwtInfo       string `xml:"grwtInfo"`
			GrwtseVeNm     string `xml:"grwtseVeNm"`
			HgtmMhmrInfo   string `xml:"hgtmMhmrInfo"`
			LfclChngeInfo  string `xml:"lfclChngeInfo"`
			LightImgUrl1   string `xml:"lightImgUrl1"`
			LightImgUrl2   string `xml:"lightImgUrl2"`
			LightImgUrl3   string `xml:"lightImgUrl3"`
			LighttInfo     string `xml:"lighttInfo"`
			MainImgUrl1    string `xml:"mainImgUrl1"`
			MainImgUrl2    string `xml:"mainImgUrl2"`
			ManageDemandNm string `xml:"manageDemandNm"`
			ManageLevelNm  string `xml:"manageLevelNm"`
			Orgplce        string `xml:"orgplce"`
			PrpgtInfo      string `xml:"prpgtInfo"`
			PswntrTpInfo   string `xml:"pswntrTpInfo"`
			RdxStleNm      string `xml:"rdxStleNm"`
			Scnm           string `xml:"scnm"`
			StleSeNm       string `xml:"stleSeNm"`
			TipInfo        string `xml:"tipInfo"`
			WaterCycleInfo string `xml:"waterCycleInfo"`
		} `xml:"item"`
	} `xml:"body"`
}
