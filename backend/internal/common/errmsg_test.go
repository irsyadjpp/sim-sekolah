package common

import (
	"errors"
	"testing"

	"github.com/gofiber/fiber/v2"
)

func TestUserMessage_AuthErrors(t *testing.T) {
	tests := []struct {
		in   string
		want string
	}{
		{"invalid email or password", "Email atau kata sandi tidak valid"},
		{"user not found", "Pengguna tidak ditemukan"},
		{"forbidden: you don't have permission to modify this resource", "Akses ditolak: Anda tidak memiliki izin mengubah resource ini"},
	}
	for _, tt := range tests {
		got := UserMessage(errors.New(tt.in))
		if got != tt.want {
			t.Errorf("UserMessage(%q) = %q, want %q", tt.in, got, tt.want)
		}
	}
}

func TestUserMessage_Prefix(t *testing.T) {
	got := UserMessage(errors.New("invalid student ID: abc-123"))
	want := "ID murid tidak valid: abc-123"
	if got != want {
		t.Errorf("got %q, want %q", got, want)
	}
}

func TestUserMessage_IndonesianPassthrough(t *testing.T) {
	in := "siswa tidak ditemukan"
	got := UserMessage(errors.New(in))
	if got != in {
		t.Errorf("got %q, want %q", got, in)
	}
}

func TestHTTPStatusFromError(t *testing.T) {
	if HTTPStatusFromError(errors.New("forbidden: x"), fiber.StatusInternalServerError) != fiber.StatusForbidden {
		t.Error("expected forbidden")
	}
	if HTTPStatusFromError(errors.New("unauthorized"), fiber.StatusInternalServerError) != fiber.StatusUnauthorized {
		t.Error("expected unauthorized")
	}
	if HTTPStatusFromError(errors.New("user not found"), fiber.StatusInternalServerError) != fiber.StatusNotFound {
		t.Error("expected not found")
	}
}

func TestIsForbidden(t *testing.T) {
	if !IsForbidden(errors.New("forbidden: you don't have permission to modify this resource")) {
		t.Error("expected forbidden")
	}
}
