package main

import (
	"context"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"time"

	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/client"
	"github.com/gin-gonic/gin"
)

type ExecutionResult struct {
	Output        string  `json:"output"`
	ExecutionTime float64 `json:"execution_time"`
	Status        string  `json:"status"`
}

func handleExecution(c *gin.Context, cli *client.Client) {

	// c.JSON(http.StatusOK, "TESTING")

	// Get files from form
	program, err := c.FormFile("program")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Program file required"})
		return
	}

	input, err := c.FormFile("input")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Input file required"})
		return
	}

	// Create temporary directory
	tempDir, err := os.MkdirTemp("", "execution-*")
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create temp directory"})
		return
	}
	defer os.RemoveAll(tempDir)

	// Save uploaded files
	programPath := filepath.Join(tempDir, "program.py")
	inputPath := filepath.Join(tempDir, "input.txt")
	// outputPath := filepath.Join(tempDir, "output.txt")

	if err := c.SaveUploadedFile(program, programPath); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save program file"})
		return
	}

	if err := c.SaveUploadedFile(input, inputPath); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save input file"})
		return
	}

	// Create container
	ctx := context.Background()
	resp, err := cli.ContainerCreate(ctx,
		&container.Config{
			Image: "python:3.9-slim",
			Cmd:   []string{"python", "/app/program.py"},
			Tty:   true,
		},
		&container.HostConfig{
			Binds: []string{
				tempDir + ":/app:ro",
			},
			Resources: container.Resources{
				Memory:   512 * 1024 * 1024, // 512MB
				NanoCPUs: 500000000,         // 0.5 CPU
			},
			NetworkMode: "none",
		},
		nil,
		nil,
		"",
	)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create container"})
		return
	}

	// Start container with timeout
	startTime := time.Now()
	if err := cli.ContainerStart(ctx, resp.ID, container.StartOptions{}); err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to start container"})
		return
	}

	// Set timeout context
	timeoutCtx, cancel := context.WithTimeout(ctx, 10*time.Second)
	defer cancel()

	// Wait for container to finish
	statusCh, errCh := cli.ContainerWait(timeoutCtx, resp.ID, container.WaitConditionNotRunning)
	var result ExecutionResult

	select {
	case err := <-errCh:
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Execution error"})
			return
		}
	case status := <-statusCh:
		result.ExecutionTime = time.Since(startTime).Seconds()
		result.Status = "success"
		if status.StatusCode != 0 {
			result.Status = "error"
		}
	case <-timeoutCtx.Done():
		c.JSON(http.StatusRequestTimeout, gin.H{"error": "Execution timeout"})
		return
	}

	// Get container logs
	out, err := cli.ContainerLogs(ctx, resp.ID, container.LogsOptions{ShowStdout: true})
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get output"})
		return
	}
	defer out.Close()

	// Read output
	output, err := io.ReadAll(out)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to read output"})
		return
	}
	result.Output = string(output)

	// Clean up container
	err = cli.ContainerRemove(ctx, resp.ID, container.RemoveOptions{Force: true})
	if err != nil {
		log.Printf("Failed to remove container: %v", err)
	}

	c.JSON(http.StatusOK, result)
}
