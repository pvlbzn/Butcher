// Attempt to make fancy image cutter.
package main

import (
	"fmt"
	"image"
	_ "image/png"
	"io/ioutil"
	"log"
	"os"
	"time"

	"gopkg.in/h2non/bimg.v0"
)

func main() {
	t1 := time.Now()
	processFiles(.5)
	t2 := time.Now()
	diff := t2.Sub(t1)
	fmt.Println("Time elapsed: ", diff)
}

func processFiles(scale float32) {
	files, err := ioutil.ReadDir("input")
	if err != nil {
		log.Fatal(err)
	}
	for _, f := range files {
		uri := "input/" + f.Name()
		w, h := getImgSize(uri, scale)
		goVips(w, h, uri, f.Name())
	}
}

func getImgSize(addr string, scale float32) (int, int) {
	file, err := os.Open(addr)
	if err != nil {
		log.Fatal("33", err)
	}
	img, _, err := image.DecodeConfig(file)
	if err != nil {
		log.Fatal(addr, err)
	}
	w := float32(img.Width) * scale
	h := float32(img.Height) * scale
	return int(w), int(h)
}

func goVips(w, h int, addr, name string) {
	buffer, err := bimg.Read(addr)
	if err != nil {
		log.Fatal(err)
	}
	img, err := bimg.NewImage(buffer).Resize(w, h)
	if err != nil {
		log.Fatal(err)
	}
	bimg.Write("output/"+name, img)
}
