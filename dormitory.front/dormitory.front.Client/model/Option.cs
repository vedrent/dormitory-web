namespace dormitory.front.Client.model
{
    public class Option
    {
        public string Title { get; set; }
        public string Description { get; set; }
        public string IconUrl { get; set; }

        public Option(string title, string description, string iconUrl) {
            Title = title;
            Description = description;
            IconUrl = iconUrl;
        }
    }
}
