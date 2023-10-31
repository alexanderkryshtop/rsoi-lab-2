package application

import (
	"context"
	"fmt"
	"github.com/jackc/pgx/v5/pgxpool"
	"os"
	"os/signal"
	"rating/cmd/configuration"
	"rating/internal/handlers"
	"rating/internal/repository"
	"rating/internal/service"
	"syscall"

	"go.uber.org/zap"
	"golang.org/x/sync/errgroup"
)

type App struct {
	Config *configuration.Config
	Logger *zap.SugaredLogger
	Pool   *pgxpool.Pool
}

func New(cfg *configuration.Config, logger *zap.SugaredLogger, pool *pgxpool.Pool) *App {
	return &App{
		Config: cfg,
		Logger: logger,
		Pool:   pool,
	}
}

func (a *App) ratingHandler() *handlers.Handler {
	ratingRepository := repository.NewRatingRepository(a.Pool)
	ratingService := service.NewRatingService(ratingRepository)
	ratingHandler := handlers.NewHandler(ratingService)
	return ratingHandler
}

func (a *App) Run() error {
	libraryHandler := a.ratingHandler()
	server, err := a.newHTTPServer(libraryHandler)
	if err != nil {
		return fmt.Errorf("new httpServer: %w", err)
	}

	wg, ctx := errgroup.WithContext(context.Background())
	wg.Go(func() error {
		return server.Run(ctx)
	})

	signalsCh := subscribeSignals()
	wg.Go(func() error {
		select {
		case sig := <-signalsCh:
			a.Logger.Infof("app received external signal for shutdown %v\n", sig)
			return fmt.Errorf("shutdown by external signal %v", sig)
		case <-ctx.Done():
			return nil
		}
	})

	return wg.Wait()
}

func subscribeSignals() <-chan os.Signal {
	signalsCh := make(chan os.Signal, 1)
	signal.Notify(signalsCh, syscall.SIGINT, syscall.SIGTERM)
	return signalsCh
}
