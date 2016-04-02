/*
Butcher takes a path of an image, its name and original DPI. It produces
an output folder with folders, each child folder is represents DPI in range
from the original DPI to the LDPI with a name "drawable-(n)" where n is DPI.
*/
package butcher

import (
	"image"
	"image/png"
	"log"
	"os"

	"github.com/nfnt/resize"
)

type Img struct {
	Name string
	NDPI string // lower case acronym
	Path string
	M    *image.Image
	W    int
	H    int
}

var DPI = [6]string{"ldpi", "mdpi", "hdpi", "xhdpi", "xxhdpi", "xxxhdpi"}
var SCL = map[string]float32{"ldpi": .75, "mdpi": 1.0, "hdpi": 1.5,
	"xhdpi": 2.0, "xxhdpi": 3.0, "xxxhdpi": 4.0}

// Take an image and scale it to different scales.
func Butch(path, name, userDPI string) {
	img := new(Img)
	img.Name = name
	img.NDPI = userDPI
	img.Path = path

	// Name of the current operation.
	folderN := "output"
	createDir(folderN)

	// Find DPI which should be processed.
	DPIRange := DPI[:findDPI(img.NDPI)]

	// Open the image, get its size.
	img.M = openImage(img.Path)
	img.W, img.H = getSize(img.M)

	// Get MDPI sizes.
	mW, mH := toMDPI(img.W, img.H, img.NDPI)
	for _, dpi := range DPIRange {
		scale := SCL[dpi]
		// Compute particular size according to the scale.
		nW := mW * scale
		nH := mH * scale
		// Scale the image.
		resImg := resizeImg(*img.M, nW, nH)
		// Write it.
		writeImg(&resImg, dpi, name)
	}
}

func createDir(fName string) {
	// Check is folder exists or not
	stat, _ := os.Stat(fName)
	if stat == nil {
		os.Mkdir(fName, os.ModePerm)
	}
}

func openImage(path string) *image.Image {
	file, err := os.Open(path)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	m, err := png.Decode(file)
	if err != nil {
		log.Fatal(err)
	}
	return &m
}

func getSize(img *image.Image) (int, int) {
	i := *img
	m := i.Bounds()
	return m.Max.X, m.Max.Y
}

func toMDPI(w, h int, DPI string) (float32, float32) {
	mw := float32(w) / SCL[DPI]
	mh := float32(h) / SCL[DPI]
	return mw, mh
}

func findDPI(d string) int {
	for i, item := range DPI {
		if item == d {
			return i + 1
		}
	}
	return 0
}

func resizeImg(img image.Image, toW, toH float32) image.Image {
	return resize.Resize(uint(toW), uint(toH), img, resize.Bilinear)
}

func writeImg(img *image.Image, DPI, imgName string) {
	fName := "output/drawable-" + DPI
	createDir(fName)
	out, err := os.Create(fName + "/" + imgName)
	if err != nil {
		log.Fatal(err)
	}
	defer out.Close()
	png.Encode(out, *img)
}
