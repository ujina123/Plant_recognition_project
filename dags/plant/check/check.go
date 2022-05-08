// JngMkk
package check

import (
	"log"
	"net/http"
)

func CheckErr(err error) {
	if err != nil {
		log.Fatalln(err)
	}
}

func CheckRes(res *http.Response) {
	if res.StatusCode != 200 {
		log.Fatalln("Request failed with Status:", res.StatusCode)
	}
}
