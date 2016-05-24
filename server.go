package main

import (
	"crypto/md5"
	"fmt"
	"html/template"
	"io"
	"net/http"
	"os"
	"strconv"
	"time"
)

var teamplates = template.Must(template.ParseFiles("template/upload.html"))

func main() {
	http.HandleFunc("/", rootHandler)
	http.HandleFunc("/upload", uploadHandler)
	//http.HandleFunc("/result", resultHandler)
	http.ListenAndServe(":24000", nil)
}

func rootHandler(w http.ResponseWriter, r *http.Request) {
	http.Redirect(w, r, "/upload", http.StatusTemporaryRedirect)
}

func uploadHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Println("method:", r.Method)
	if r.Method == "GET" {
		t := time.Now().Unix()
		h := md5.New()
		io.WriteString(h, strconv.FormatInt(t, 10))
		token := fmt.Sprintf("%x", h.Sum(nil))
		teamplates.ExecuteTemplate(w, "upload.html", token)
	} else {
		r.ParseMultipartForm(32 << 20)
		file, handler, err := r.FormFile("uploadfile")
		if err != nil {
			errorHandler(w, r, http.StatusNotFound, err)
			return
		}
		defer file.Close()
		fmt.Fprintf(w, "%v", handler.Header)
		f, err := os.OpenFile("./upl/"+handler.Filename, os.O_WRONLY|os.O_CREATE, 0666)
		if err != nil {
			errorHandler(w, r, http.StatusInternalServerError, err)
			return
		}
		defer f.Close()
		io.Copy(f, file)
	}
}

func errorHandler(w http.ResponseWriter, r *http.Request, status int, err error) {
	switch status {
	case http.StatusNotFound:
		http.NotFound(w, r)
		fmt.Println(err)
	case http.StatusInternalServerError:
		http.Error(w, err.Error(), http.StatusInternalServerError)
		fmt.Println(err)
	default:
		return
	}
}
