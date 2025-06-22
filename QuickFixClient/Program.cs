using FixClientService.Sessions;

public class App
{
    private InitializeFixClient? _fixInstance;
    private readonly CancellationTokenSource _cts = new();

    public async Task StartApp()
    {
        try
        {
            _fixInstance = new InitializeFixClient();

            // Start FIX client session in a new thread
            var fixThread = new Thread(() => _fixInstance.StartFixSession());
            fixThread.Start();

            // Optionally wait a bit
            await Task.Delay(10000);

            // Correct: Call SendMessage on _fixInstance
            _fixInstance.SendMessage(
                "PETR4",
                "LMT",
                10m,
                "BUY"
            );

            Console.WriteLine("FIX client session started.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error starting application: {ex.Message}");
        }
    }

    public Task StopApp()
    {
        try
        {
            Console.WriteLine("Stopping application...");
            _cts.Cancel();  // Signal cancellation
            _fixInstance?.StopFixSession();
            Console.WriteLine("Application stopped.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error stopping application: {ex.Message}");
        }

        return Task.CompletedTask;
    }
}

class Program
{
    static async Task Main()
    {
        var appInstance = new App();
        appInstance.StartApp();
    }
}
