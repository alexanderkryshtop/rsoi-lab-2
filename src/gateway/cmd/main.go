package main

import (
	"gateway/cmd/application"
	"gateway/cmd/configuration"
	"log"

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

	app := application.New(config, logger)
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
