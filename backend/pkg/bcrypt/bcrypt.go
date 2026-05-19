package bcryptpkg

import (
	"sim-sekolah/config"

	"golang.org/x/crypto/bcrypt"
)

func HashPassword(password string) (string, error) {

	cost := config.Cfg.Auth.Bcrypt.Cost
	if cost == 0 {
		cost = bcrypt.DefaultCost
	}

	hashedPassword, err := bcrypt.GenerateFromPassword(
		[]byte(password),
		cost,
	)

	if err != nil {
		return "", err
	}

	return string(hashedPassword), nil
}

func CheckPassword(hash string, password string) bool {

	err := bcrypt.CompareHashAndPassword(
		[]byte(hash),
		[]byte(password),
	)

	return err == nil
}
