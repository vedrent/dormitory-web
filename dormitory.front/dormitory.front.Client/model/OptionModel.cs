namespace dormitory.front.Client.model
{
    public class OptionModel
    {
        public string Title { get; set; }
        public string Description { get; set; }
        public string IconUrl { get; set; }

        public string Path { get; set; }
        public OptionModel(string title, string description, string iconUrl, string path)
        {
            Title = title;
            Description = description;
            IconUrl = iconUrl;
            Path = path;
        }
    }
}
