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

            // Start FIX client session
            var fixThread = new Thread(() => _fixInstance.StartFixSession());
            fixThread.Start();

            Console.WriteLine("FIX client session started.");

            // UI runs on the main thread
            var form2 = new MyWinFormsApp.Form2();
            form2.Show();

            Application.Run(new MyWinFormsApp.Form1(_fixInstance, form2));

            // Wait for UI to close before stopping the app
            await StopApp();
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
    [STAThread]  // Required for Windows Forms
    static async Task Main()
    {
        ApplicationConfiguration.Initialize();  // Must be before UI launch

        var appInstance = new App();
        await appInstance.StartApp();
    }
}
