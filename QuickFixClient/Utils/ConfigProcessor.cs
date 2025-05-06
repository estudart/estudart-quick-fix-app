

namespace QuickFixClient.Utils
{
    public static class ConfigProcessor
    {
        public static string ProcessConfig(string templatePath)
        {
            string outputPath = templatePath.Replace(".template", "");

            string hostPort = Environment.GetEnvironmentVariable("HOST_PORT") ?? "8080";

            string configContent = File.ReadAllText(templatePath);

            configContent = configContent
                .Replace("HOST_PORT", hostPort);

            File.WriteAllText(outputPath, configContent);

            Console.WriteLine($"Config file processed and saved to {outputPath}");

            return outputPath;
        }
    }
}
