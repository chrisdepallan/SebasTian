# SebasTian

An intelligent personal assistant powered by OpenAI's GPT that helps users set and achieve goals, manage tasks, and stay on top of important events.

## Features

- 🎯 Smart Goal Setting: AI-powered guidance for setting SMART goals
- ⏰ Event Reminders: Intelligent event tracking and timely notifications
- ✅ Task Management: Progress monitoring and adaptive task scheduling
- 📊 Progress Analytics: Track your goal completion and productivity metrics
- 🤖 AI-Powered Insights: Personalized recommendations and motivation

## Getting Started

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- MongoDB (for storing user data and conversations)
- Git

### Installation

#### Linux Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/chrisdepallan/sebastian.git
   cd sebastian
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   nano .env
   ```
   Add your configuration:
   ```
   OPENAI_API_KEY=your_api_key_here
   MONGODB_URI=your_mongodb_connection_string
   ```

5. Set up systemd service for auto-start:
   ```bash
   sudo nano /etc/systemd/system/sebastian.service
   ```
   Add the following content:
   ```ini
   [Unit]
   Description=SebasTian Assistant
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/path/to/sebastian
   Environment="PATH=/path/to/sebastian/venv/bin"
   ExecStart=/path/to/sebastian/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000

   [Install]
   WantedBy=multi-user.target
   ```

6. Enable and start the service:
   ```bash
   sudo systemctl enable sebastian.service
   sudo systemctl start sebastian.service
   ```

#### Windows Installation

1. Install Git and Python from their official websites if not already installed.

2. Clone the repository:
   ```cmd
   git clone https://github.com/chrisdepallan/sebastian.git
   cd sebastian
   ```


3. Create and activate virtual environment:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. Install required dependencies:
   ```cmd
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   ```cmd
   copy .env.example .env
   ```
   Edit `.env` with your preferred text editor and add:
   ```
   OPENAI_API_KEY=your_api_key_here
   MONGODB_URI=your_mongodb_connection_string
   ```

6. Create startup script:
   ```cmd
   echo @echo off > start_sebastian.bat
   echo cd %~dp0 >> start_sebastian.bat
   echo call venv\Scripts\activate >> start_sebastian.bat
   echo uvicorn src.main:app --host 0.0.0.0 --port 8000 >> start_sebastian.bat
   ```

7. Create shortcut to startup folder:
   - Press `Win + R`
   - Type `shell:startup`
   - Create shortcut to `start_sebastian.bat`

## Usage

1. Access the web interface:
   ```
   http://localhost:8000
   ```

2. API endpoints:
   ```bash
   # Set goals
   curl -X POST http://localhost:8000/goals -d '{"goal": "Learn Python in 3 months"}'

   # Add tasks
   curl -X POST http://localhost:8000/tasks -d '{"task": "Complete Python basics tutorial"}'

   # Set reminders
   curl -X POST http://localhost:8000/reminders -d '{"title": "Team meeting", "datetime": "2024-03-20 14:00"}'
   ```

## Configuration

You can customize SebasTian's behavior through the `config.yaml` file:

- Reminder preferences
- Goal tracking frequency
- AI interaction style
- Notification settings
- API rate limits
- Database settings

## Troubleshooting

### Common Issues

1. Service won't start:
   - Check logs: `sudo journalctl -u sebastian.service`
   - Verify paths in service file
   - Ensure proper permissions

2. API connection issues:
   - Verify API key in .env
   - Check network connectivity
   - Confirm port availability

## Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- GitHub Issues: [Create an issue](https://github.com/chrisdepallan/sebastian/issues)
- Documentation: [Wiki](https://github.com/yourusername/sebastian/wiki)
- Community: [Discussions](https://github.com/yourusername/sebastian/discussions)