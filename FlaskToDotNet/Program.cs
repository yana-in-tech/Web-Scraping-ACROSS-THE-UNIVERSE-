// Program.cs (ASP.NET Core Web API)
using Microsoft.AspNetCore.Mvc;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// 1. Define C# Models (Strong types catch errors before runtime)
public record ScrapedItemDto(string Id, string Title, string Url);
public record IngestionPayloadDto(string SourceUrl, List<ScrapedItemDto> Items);

// 2. The Fast Ingestion Endpoint Flask calls
app.MapPost("/api/data-ingestion", async (
    [FromHeader(Name = "X-Internal-Secret")] string secret,
    [FromBody] IngestionPayloadDto payload) =>
{
    // Basic authorization check for internal service communication
    if (secret != "SuperSecureToken123")
    {
        return Results.Unauthorized();
    }

    if (payload?.Items == null || !payload.Items.Any())
    {
        return Results.BadRequest("Payload contains no items.");
    }

    // Process the data at lightning speed
    // This is where you would perform bulk inserts to PostgreSQL or index into Elasticsearch
    Console.WriteLine($"[INFO] Received {payload.Items.Count} items from {payload.SourceUrl}");
    
    foreach (var item in payload.Items.Take(3)) // Previewing first few items
    {
        Console.WriteLine($" -> [{item.Id}] {item.Title}");
    }

    // Wipe/Invalidate Redis Cache here so frontend clients instantly pull new updates
    // await cache.InvalidateAsync("homepage_search_results");

    return Results.Ok(new { message = "Data ingested, processed, and cache flushed." });
});

app.Run("http://localhost:
5123");
