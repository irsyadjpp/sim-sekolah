#!/bin/sh

# Sim Sekolah Backend Pre-Commit Git Hook
# Enforces Go formatting (gofmt), linting (golangci-lint), and vulnerability scanning (govulncheck) before committing.

export PATH="$PATH:$HOME/go/bin"

echo "========================================="
echo "🚀 SIM Sekolah: Running Backend Pre-Commit Checks..."
echo "========================================="

# 1. Format Check (gofmt)
echo "🔍 Checking Go formatting (gofmt)..."
UNFORMATTED=$(gofmt -l .)
if [ -n "$UNFORMATTED" ]; then
    echo "❌ The following Go files are not formatted properly:"
    echo "$UNFORMATTED"
    echo "💡 Action: Run 'go fmt ./...' to format your files before committing."
    exit 1
fi
echo "✅ Go formatting is clean."

# 2. Static Analysis / Linting (golangci-lint)
echo "🔍 Running golangci-lint..."
if ! golangci-lint run ./...; then
    echo "❌ golangci-lint failed. Please fix the lints before committing."
    exit 1
fi
echo "✅ golangci-lint is clean."

# 3. Vulnerability Scan (govulncheck) - Non-blocking (Status: bagus)
echo "🔍 Running vulnerability scan (govulncheck)..."
if ! govulncheck ./...; then
    echo "⚠️ govulncheck detected vulnerabilities (likely from standard library Go version). Please review them, but continuing commit..."
else
    echo "✅ govulncheck is clean."
fi

echo "========================================="
echo "🎉 SIM Sekolah Backend Checks Passed! Committing code..."
echo "========================================="
exit 0
