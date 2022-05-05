package plantinfo

import "encoding/xml"

type PlantList struct {
	PlCode string
	PlName string
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

type PlantInfo struct {
	PlCode        string // 식물코드
	DivName       string // 분류명
	EclgyName     string // 생태명
	Height        string // 성장 높이
	Area          string // 성장 넓이
	FlColor       string // 꽃색
	FlSeason      string // 꽃피는 시기
	SmellCode     string // 냄새 코드
	LightDemand   string // 광요구정도
	Place         string // 위치
	Toxic         string // 독성
	LevelCode     string // 관리자 숙련도
	GrowSpeedCode string // 성장속도 코드
	GrowTempCode  string // 성장온도 코드
	WinterLowCode string // 겨울 최저온도 코드
	HumidityCode  string // 습도 코드
	SpringWtCode  string // 봄 물주기 코드
	SummerWtCode  string // 여름 물주기 코드
	AutumnWtCode  string // 가을 물주기 코드
	WinterWtCode  string // 겨울 물주기 코드
	SpeclManage   string // 설명
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
			Text                          string `xml:",chardata"`
			AdviseInfo                    string `xml:"adviseInfo"`
			ClCodeNm                      string `xml:"clCodeNm"`
			CntntsNo                      string `xml:"cntntsNo"`
			DistbNm                       string `xml:"distbNm"`
			DlthtsCodeNm                  string `xml:"dlthtsCodeNm"`
			DlthtsManageInfo              string `xml:"dlthtsManageInfo"`
			EclgyCodeNm                   string `xml:"eclgyCodeNm"`
			EtcEraInfo                    string `xml:"etcEraInfo"`
			FlclrCodeNm                   string `xml:"flclrCodeNm"`
			FlpodmtBigInfo                string `xml:"flpodmtBigInfo"`
			FlpodmtMddlInfo               string `xml:"flpodmtMddlInfo"`
			FlpodmtSmallInfo              string `xml:"flpodmtSmallInfo"`
			FmlCodeNm                     string `xml:"fmlCodeNm"`
			FmlNm                         string `xml:"fmlNm"`
			FmldeSeasonCodeNm             string `xml:"fmldeSeasonCodeNm"`
			FmldecolrCodeNm               string `xml:"fmldecolrCodeNm"`
			FncltyInfo                    string `xml:"fncltyInfo"`
			FrtlzrInfo                    string `xml:"frtlzrInfo"`
			GrowthAraInfo                 string `xml:"growthAraInfo"`
			GrowthHgInfo                  string `xml:"growthHgInfo"`
			GrwhTpCode                    string `xml:"grwhTpCode"`
			GrwhTpCodeNm                  string `xml:"grwhTpCodeNm"`
			GrwhstleCodeNm                string `xml:"grwhstleCodeNm"`
			GrwtveCode                    string `xml:"grwtveCode"`
			GrwtveCodeNm                  string `xml:"grwtveCodeNm"`
			HdCode                        string `xml:"hdCode"`
			HdCodeNm                      string `xml:"hdCodeNm"`
			HgBigInfo                     string `xml:"hgBigInfo"`
			HgMddlInfo                    string `xml:"hgMddlInfo"`
			HgSmallInfo                   string `xml:"hgSmallInfo"`
			IgnSeasonCodeNm               string `xml:"ignSeasonCodeNm"`
			ImageEvlLinkCours             string `xml:"imageEvlLinkCours"`
			IndoorpsncpacompositionCodeNm string `xml:"indoorpsncpacompositionCodeNm"`
			LefStleInfo                   string `xml:"lefStleInfo"`
			LefcolrCodeNm                 string `xml:"lefcolrCodeNm"`
			LefmrkCodeNm                  string `xml:"lefmrkCodeNm"`
			LighttdemanddoCodeNm          string `xml:"lighttdemanddoCodeNm"`
			ManagedemanddoCode            string `xml:"managedemanddoCode"`
			ManagedemanddoCodeNm          string `xml:"managedemanddoCodeNm"`
			ManagelevelCode               string `xml:"managelevelCode"`
			ManagelevelCodeNm             string `xml:"managelevelCodeNm"`
			OrgplceInfo                   string `xml:"orgplceInfo"`
			PcBigInfo                     string `xml:"pcBigInfo"`
			PcMddlInfo                    string `xml:"pcMddlInfo"`
			PcSmallInfo                   string `xml:"pcSmallInfo"`
			PlntbneNm                     string `xml:"plntbneNm"`
			PlntzrNm                      string `xml:"plntzrNm"`
			PostngplaceCodeNm             string `xml:"postngplaceCodeNm"`
			PrpgtEraInfo                  string `xml:"prpgtEraInfo"`
			PrpgtmthCodeNm                string `xml:"prpgtmthCodeNm"`
			SmellCode                     string `xml:"smellCode"`
			SmellCodeNm                   string `xml:"smellCodeNm"`
			SoilInfo                      string `xml:"soilInfo"`
			SpeclmanageInfo               string `xml:"speclmanageInfo"`
			ToxctyInfo                    string `xml:"toxctyInfo"`
			VolmeBigInfo                  string `xml:"volmeBigInfo"`
			VolmeMddlInfo                 string `xml:"volmeMddlInfo"`
			VolmeSmallInfo                string `xml:"volmeSmallInfo"`
			VrticlBigInfo                 string `xml:"vrticlBigInfo"`
			VrticlMddlInfo                string `xml:"vrticlMddlInfo"`
			VrticlSmallInfo               string `xml:"vrticlSmallInfo"`
			WatercycleAutumnCode          string `xml:"watercycleAutumnCode"`
			WatercycleAutumnCodeNm        string `xml:"watercycleAutumnCodeNm"`
			WatercycleSprngCode           string `xml:"watercycleSprngCode"`
			WatercycleSprngCodeNm         string `xml:"watercycleSprngCodeNm"`
			WatercycleSummerCode          string `xml:"watercycleSummerCode"`
			WatercycleSummerCodeNm        string `xml:"watercycleSummerCodeNm"`
			WatercycleWinterCode          string `xml:"watercycleWinterCode"`
			WatercycleWinterCodeNm        string `xml:"watercycleWinterCodeNm"`
			WidthBigInfo                  string `xml:"widthBigInfo"`
			WidthMddlInfo                 string `xml:"widthMddlInfo"`
			WidthSmallInfo                string `xml:"widthSmallInfo"`
			WinterLwetTpCode              string `xml:"winterLwetTpCode"`
			WinterLwetTpCodeNm            string `xml:"winterLwetTpCodeNm"`
		} `xml:"item"`
	} `xml:"body"`
}
