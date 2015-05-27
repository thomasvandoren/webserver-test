// Go web server implementation.
//
// To install dependencies:
//
//     go get code.google.com/p/go-uuid/uuid
//     go get github.com/gorilla/mux
//

package main

import (
	"encoding/json"
	"net/http"
	"time"

	"code.google.com/p/go-uuid/uuid"
	"github.com/gorilla/mux"
)

type MyData struct {
	UTCDatetime string
	UUID        string
}

func main() {
	r := mux.NewRouter().StrictSlash(true)
	r.HandleFunc("/", getHandler)

	u := r.Path("/uuid/{theUuid}").Subrouter()
	u.Methods("POST").HandlerFunc(postHandler)

	http.ListenAndServe(":5000", r)
}

func getHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, "", http.StatusMethodNotAllowed)
		return
	}

	d := MyData{utcnow(), uuid.New()}
	respond(d, w)
}

func postHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "", http.StatusMethodNotAllowed)
		return
	}

	theUuid := uuid.Parse(mux.Vars(r)["theUuid"])
	if theUuid == nil {
		http.Error(w, "Could not parser UUID", http.StatusBadRequest)
		return
	}

	d := MyData{utcnow(), theUuid.String()}
	respond(d, w)
}

func utcnow() string {
	return time.Now().UTC().Format("2006-01-02T15:04:05")
}

func respond(d MyData, w http.ResponseWriter) {
	js, err := json.Marshal(d)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write(js)
}
