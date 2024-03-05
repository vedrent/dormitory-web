using System.Net;
using System.Net.Http.Headers;
using System.Net.Http;
using Microsoft.AspNetCore.Components;
using Newtonsoft.Json;

namespace dormitory.front.Client.model;

public interface IAuth
{
    public Task<bool> Authorize();
}
public class Auth : IAuth
{
    readonly ICookie cookie;
    readonly HttpClient httpClient;
    readonly IAccount account;
    public Auth(ICookie cookie, HttpClient httpClient, IAccount account)
    {
        this.cookie = cookie;
        this.httpClient = httpClient;
        this.account = account;
    }
    public async Task<bool> Authorize()
    {
        AuthorizationModel model = await ReadTokenAsync();
        httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", model.access_token);
        var responseAuth = await httpClient.GetAsync("http://localhost:6981/whoami");
        var jsonResponse = await responseAuth.Content.ReadAsStringAsync();
        account.Current = JsonConvert.DeserializeObject<AccountModel>(jsonResponse);
        return responseAuth.IsSuccessStatusCode;
        
    }
    async Task<AuthorizationModel> ReadTokenAsync()
    {
        AuthorizationModel model = new AuthorizationModel();
        model.access_token = await cookie.GetValueAsync("access_token");
        model.refresh_token = await cookie.GetValueAsync("refresh_token");
        return model;
    }
}

public class AuthorizationModel
{
    public string access_token;
    public string refresh_token;
}

public class AuthData
{
    public string username { get; set; } = "";
    public string password { get; set; } = "";
}
