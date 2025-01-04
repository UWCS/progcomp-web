package main

import (
	"log"

	"github.com/docker/docker/client"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	// Initialize Docker client
	// cli, err := client.NewClientWithOpts(client.FromEnv)
	cli, err := client.NewClientWithOpts(client.FromEnv)
	if err != nil {
		log.Fatal(err)
	}

	r.POST("/execute", func(c *gin.Context) {
		handleExecution(c, cli)
	})

	r.Run(":8080")
}
