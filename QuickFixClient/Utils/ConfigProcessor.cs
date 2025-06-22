

namespace QuickFixClient.Utils
{
    public static class ConfigProcessor
    {
        public static string ProcessConfig(string templatePath)
        {
            string outputPath = templatePath.Replace(".template", "");

            string port = Environment.GetEnvironmentVariable("PORT") ?? "8080";

            string host = Environment.GetEnvironmentVariable("HOST") ?? "host.docker.internal";

            string configContent = File.ReadAllText(templatePath);

            configContent = configContent
                .Replace("HOST", host);

            configContent = configContent
                .Replace("PORT", port);

            File.WriteAllText(outputPath, configContent);

            Console.WriteLine($"Config file processed and saved to {outputPath}");

            return outputPath;
        }
    }
}
