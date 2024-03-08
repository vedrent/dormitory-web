namespace dormitory.front.Client.model;

public class Washer
{
    public Washer(int id, int status)
    {
        this.id = id;
        this.status = status;
    }

    public int id { get; set; }
    /// <summary>
    /// status: 0 - broken, 1 - ready, 2 - busy
    /// </summary>
    public int status { get; set; }


}