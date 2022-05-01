// JngMkk kakao coord to addr
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)

type region struct {
	Meta struct {
		TotalCount int `json:"total_count"`
	} `json:"meta"`
	Documents []struct {
		RoadAddress interface{} `json:"road_address"`
		Address     struct {
			AddressName      string `json:"address_name"`
			Region1DepthName string `json:"region_1depth_name"`
			Region2DepthName string `json:"region_2depth_name"`
			Region3DepthName string `json:"region_3depth_name"`
			MountainYn       string `json:"mountain_yn"`
			MainAddressNo    string `json:"main_address_no"`
			SubAddressNo     string `json:"sub_address_no"`
			ZipCode          string `json:"zip_code"`
		} `json:"address"`
	} `json:"documents"`
}

func coordToAddr(lng, lat string) []string {
	url := fmt.Sprintf("https://dapi.kakao.com/v2/local/geo/coord2address.json?x=%s&y=%s", lng, lat)
	res, err := http.NewRequest("GET", url, nil)
	if err != nil {
		panic(err)
	}

	res.Header.Add("Authorization", "KakaoAK ")

	client := &http.Client{}
	resp, err := client.Do(res)
	if err != nil {
		panic(err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		panic(err)
	}

	var r region

	if err := json.Unmarshal(body, &r); err != nil {
		panic(err)
	}

	addr := strings.Split(r.Documents[0].Address.AddressName, " ")
	return addr
}

func main() {

	addr := coordToAddr("128.60355277777776", "35.868541666666665")

	fmt.Println(addr)

}
