using dormitory.front.Client.model;
using Microsoft.AspNetCore.Components.WebAssembly.Hosting;
using Microsoft.JSInterop;

var builder = WebAssemblyHostBuilder.CreateDefault(args);
builder.Services.AddScoped(sp =>
    new HttpClient
    {
        BaseAddress = new Uri("https://localhost")
    });
builder.Services.AddSingleton<IAccount, Account>();
builder.Services.AddScoped<ICookie, Cookie>();
builder.Services.AddScoped<IAuth, Auth>();

await builder.Build().RunAsync();
