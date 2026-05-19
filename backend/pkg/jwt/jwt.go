package jwt

import (
	"sim-sekolah/config"
	"time"

	jwtlib "github.com/golang-jwt/jwt/v5"
)

type JWTClaim struct {
	UserID   string   `json:"user_id"`
	Username string   `json:"username"`
	Roles    []string `json:"roles"`
	jwtlib.RegisteredClaims
}

func GenerateToken(userID string, username string, roles []string) (string, error) {
	expireHour := config.Cfg.Auth.JWT.ExpireHour
	if expireHour == 0 {
		expireHour = 24
	}

	claims := JWTClaim{
		UserID:   userID,
		Username: username,
		Roles:    roles,
		RegisteredClaims: jwtlib.RegisteredClaims{
			ExpiresAt: jwtlib.NewNumericDate(time.Now().Add(time.Hour * time.Duration(expireHour))),
			IssuedAt:  jwtlib.NewNumericDate(time.Now()),
		},
	}

	token := jwtlib.NewWithClaims(jwtlib.SigningMethodHS256, claims)

	secret := config.Cfg.Auth.JWT.Secret
	if secret == "" {
		secret = "4f9d7c2b1a8e6f5d9c3b7e1a2f4c8d6e9b1f3a7c5d8e2f6a1b9c4d7e8f2a6c1"
	}

	return token.SignedString([]byte(secret))
}

// ParseToken validates and decodes a JWT string, returning its claims.
func ParseToken(tokenStr string) (*JWTClaim, error) {
	secret := config.Cfg.Auth.JWT.Secret
	if secret == "" {
		secret = "4f9d7c2b1a8e6f5d9c3b7e1a2f4c8d6e9b1f3a7c5d8e2f6a1b9c4d7e8f2a6c1"
	}

	claims := &JWTClaim{}
	_, err := jwtlib.ParseWithClaims(tokenStr, claims, func(t *jwtlib.Token) (interface{}, error) {
		return []byte(secret), nil
	})
	if err != nil {
		return nil, err
	}
	return claims, nil
}
