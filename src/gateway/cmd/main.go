package main

import (
	"fmt"
	"gateway/cmd/application"
	"gateway/cmd/configuration"
	"io"
	"log"
	"net/http"

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

	err = pingServices(config)
	if err != nil {
		log.Fatalf("failed to connect to service: %+v", err)
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

func pingServices(cfg *configuration.Config) error {
	reservationService := cfg.ReservationService
	libraryService := cfg.LibraryService
	ratingService := cfg.RatingService

	for _, service := range []configuration.EndpointConfig{reservationService, libraryService, ratingService} {
		url := fmt.Sprintf("http://%s:%d/admin/ping", service.Address, service.Port)
		err := pingService(url)
		if err != nil {
			return err
		}
	}
	return nil
}

func pingService(url string) error {
	resp, err := http.Get(url)
	if err != nil {
		return fmt.Errorf("cannot connect to %s: %+v", url, err)
	}
	defer func(Body io.ReadCloser) {
		_ = Body.Close()
	}(resp.Body)

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("connection to %s: status code is not %d", url, http.StatusOK)
	}
	return nil
}
