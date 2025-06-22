# Use the .NET 8 SDK image to build the application
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build

# Set the working directory inside the container
WORKDIR /app

# Copy only the .csproj file first to optimize layer caching
COPY QuickFixClient.csproj ./

# Restore dependencies
RUN dotnet restore

# Copy all source files
COPY . . 

# Build and publish the application
RUN dotnet publish QuickFixClient.csproj -c Release -o /publish --no-restore

# Use the .NET 8 runtime image to run the application
FROM mcr.microsoft.com/dotnet/runtime:8.0 AS runtime

# Set the working directory inside the runtime container
WORKDIR /publish

# Copy the published application from the build container
COPY --from=build /publish .
COPY Utils ./Utils
COPY Docs ./Docs
COPY Store ./Store


# Run the application
CMD ["dotnet", "QuickFixClient.dll"]
