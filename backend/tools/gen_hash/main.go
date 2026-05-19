package main

import (
	"fmt"
	"sim-sekolah/pkg/bcrypt"
)

func main() {
	hash, err := bcryptpkg.HashPassword("admin123")
	if err != nil {
		panic(err)
	}
	fmt.Println(hash)
}
