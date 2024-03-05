namespace dormitory.front.Client.model;

public interface IAccount
{
    public AccountModel Current { get; set; }
    public bool IsEmpty { get; set; }
    public void Clear();
}

public class Account : IAccount
{
    private AccountModel current;

    public AccountModel Current
    {
        get { return current; }
        set
        {
            current = value;
            IsEmpty = false;
        }
    }
    public bool IsEmpty { get; set; }
    public Account()
    {
        Clear();
    }
    public void Clear()
    {
        Current = new AccountModel(0, "", "");
        IsEmpty = true;
    }
}

public class AccountModel
{
    public int id;
    public string username;
    public string role;
    public AccountModel(int id, string username, string role)
    {
        this.id = id;
        this.username = username;
        this.role = role;
    }

  
}