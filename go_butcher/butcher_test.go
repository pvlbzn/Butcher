/*
Tests test every function as well as overall functionality. It creates
folder, generates few images in it, and tests butcher functionality.
*/
package butcher

import (
	"image"
	"image/png"
	"io/ioutil"
	"log"
	"os"
	"testing"
)

const (
	tDir string = "testDirectory"
)

func delTestEnv(n string) {
	os.RemoveAll(n)
}

func TestCreateDir(t *testing.T) {
	if stat, _ := os.Stat(tDir); stat == nil {
		createDir(tDir)
		if stat, _ = os.Stat(tDir); stat == nil {
			t.Error("Dirictory wasn't created.")
		}
	}
}

func generateImg(w, h int, d, n string) {
	path := d + "/" + n + ".png"
	f, err := os.OpenFile(path, os.O_CREATE|os.O_WRONLY, 0666)
	if err != nil {
		log.Fatal(err)
		os.Exit(1)
	}
	m := image.NewRGBA(image.Rect(0, 0, w, h))
	if err = png.Encode(f, m); err != nil {
		log.Fatal(err)
		os.Exit(1)
	}
}

func TestParseImgNames(t *testing.T) {
	generateImg(250, 250, tDir, "img1")
	generateImg(250, 250, tDir, "img2")
	if r := parseImgNames(tDir); r[0] != "img1.png" && r[1] != "img2.png" {
		t.Error("Images not found.")
	}
}

func TestOpenImage(t *testing.T) {
	path := tDir + "/" + "img1.png"
	if m := openImage(path); m == nil {
		t.Error("Image doesn't opened.")
	}
}

func TestGetSize(t *testing.T) {
	path := tDir + "/" + "img1.png"
	m := openImage(path)
	if w, h := getSize(m); w != 250 && h != 250 {
		t.Error("Wrong sizes.")
	}
}

func TestToMDPI(t *testing.T) {
	if w, h := toMDPI(250, 250, "mdpi"); uint(w) != 250 && uint(h) != 250 {
		t.Error("Wrong MDPI")
	}
	if w, h := toMDPI(250, 250, "hdpi"); uint(w) != 166 && h != 166 {
		t.Error("Wrong HDPI")
	}
	if w, h := toMDPI(250, 250, "xxxhdpi"); uint(w) != 62 && uint(h) != 62 {
		t.Error("Wrong XXXHDPI")
	}
}

func parseImgNames(folder string) []string {
	f, err := ioutil.ReadDir(folder)
	if err != nil {
		log.Fatal(err)
	}
	content := []string{}
	for _, file := range f {
		if n := string(file.Name()); string(n[0]) != "." {
			content = append(content, n)
		}
	}
	return content
}

func TestButch(t *testing.T) {
	f := parseImgNames(tDir)
	for _, name := range f {
		path := tDir + "/" + name
		Butch(path, name, "xxxhdpi")
	}
	delTestEnv(tDir)
}
