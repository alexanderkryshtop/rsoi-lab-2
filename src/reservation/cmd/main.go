package main

import (
	"context"
	"fmt"
	"log"
	"reservation/cmd/application"
	"reservation/cmd/configuration"

	"github.com/jackc/pgx/v5/pgxpool"
	"go.uber.org/zap"
)

func main() {
	config, err := configuration.LoadConfig()
	if err != nil {
		log.Fatalf("failed to create config: %v", err)
	}

	logger, err := newLogger(config)
	if err != nil {
		log.Fatalf("failed to create logger: %v", err)
	}

	pool, err := createDBConnection()
	if err != nil {
		logger.Fatalf("failed to create database connection: %v", err)
	}
	defer pool.Close()

	app := application.New(config, logger, pool)
	if err := app.Run(); err != nil {
		logger.Infof("application stopped: %+v\n", err)
	} else {
		logger.Infof("application stopped\n")
	}
}

func newLogger(cfg *configuration.Config) (*zap.SugaredLogger, error) {
	zapConfig := zap.NewDevelopmentConfig()

	err := zapConfig.Level.UnmarshalText([]byte(cfg.Logger.Level))
	if err != nil {
		return nil, err
	}
	zapConfig.Encoding = cfg.Logger.Encoding
	zapConfig.OutputPaths = cfg.Logger.OutputPaths
	zapConfig.ErrorOutputPaths = cfg.Logger.ErrorOutputPaths
	zapConfig.DisableStacktrace = !cfg.Logger.EnableStackTrace

	logger, err := zapConfig.Build()
	if err != nil {
		return nil, err
	}
	return logger.Sugar(), nil
}

func createDBConnection() (*pgxpool.Pool, error) {
	connString := fmt.Sprintf("postgres://%s:%s@%s:%d/%s?sslmode=disable",
		"postgres",
		"postgres",
		"localhost",
		5432,
		"reservations",
	)
	pool, err := pgxpool.New(context.Background(), connString)
	if err != nil {
		return nil, err
	}
	err = pool.Ping(context.Background())
	if err != nil {
		return nil, err
	}
	return pool, err
}
