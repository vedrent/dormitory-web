namespace dormitory.front.Client.model;

public class NewsItemModel
{
    public string Title {  get; set; }
    public string Content { get; set; }
    public string Source { get; set; }

    public NewsItemModel(string title, string content, string source)
    {
        Title = title;
        Content = content;
        Source = source;
    }
}
