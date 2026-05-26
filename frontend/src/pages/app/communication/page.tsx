import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { Alert, Box, Breadcrumbs, Card, CardContent, CircularProgress, Tab, Tabs, Typography } from "@mui/material";

import { DEFAULTS } from "@/config";

interface Announcement {
  id: string;
  title: string;
  content: string;
  target_audience: string;
  priority: string;
  created_at: string;
}

interface Message {
  id: string;
  sender_id: string;
  sender_name: string;
  receiver_id: string;
  receiver_name: string;
  subject: string;
  content: string;
  is_read: boolean;
  created_at: string;
}

export default function CommunicationPage() {
  const { t } = useTranslation();
  const [tabValue, setTabValue] = useState(0);
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnnouncements = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/communication/announcements`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setAnnouncements(json.data || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const fetchMessages = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/communication/messages`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setMessages(json.data || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchAnnouncements(), fetchMessages()]);
      setLoading(false);
    };
    loadData();
  }, []);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  return (
    <Box>
      <Box className="mb-2">
        <Typography variant="h1" component="h1" className="mb-0">
          {t("communication.title")}
        </Typography>
        <Breadcrumbs className="mt-2">
          <Link color="inherit" to="/home">
            {t("communication.breadcrumb-home")}
          </Link>
          <Typography variant="body2">{t("communication.breadcrumb-communication")}</Typography>
        </Breadcrumbs>
      </Box>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <Tabs value={tabValue} onChange={handleTabChange} aria-label="communication tabs">
            <Tab label={t("communication.tab-announcements")} />
            <Tab label={t("communication.tab-messages")} />
            <Tab label={t("communication.tab-notifications")} />
          </Tabs>

          {tabValue === 0 && (
            <Box className="mt-4">
              {loading ? (
                <Box display="flex" justifyContent="center" className="py-10">
                  <CircularProgress size={24} />
                </Box>
              ) : announcements.length > 0 ? (
                <Box className="grid grid-cols-1 gap-4">
                  {announcements.map((announcement) => (
                    <Card key={announcement.id}>
                      <CardContent>
                        <Typography variant="h6" className="mb-2">
                          {announcement.title}
                        </Typography>
                        <Typography variant="body2" className="mb-2">
                          {announcement.content}
                        </Typography>
                        <Box display="flex" justifyContent="space-between">
                          <Typography variant="caption" color="textSecondary">
                            {t("communication.target")}: {announcement.target_audience}
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            {new Date(announcement.created_at).toLocaleDateString("id-ID")}
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary">
                  {t("communication.no-announcements")}
                </Typography>
              )}
            </Box>
          )}

          {tabValue === 1 && (
            <Box className="mt-4">
              {loading ? (
                <Box display="flex" justifyContent="center" className="py-10">
                  <CircularProgress size={24} />
                </Box>
              ) : messages.length > 0 ? (
                <Box className="grid grid-cols-1 gap-4">
                  {messages.map((message) => (
                    <Card key={message.id} className={message.is_read ? "opacity-60" : ""}>
                      <CardContent>
                        <Typography variant="h6" className="mb-2">
                          {message.subject}
                        </Typography>
                        <Typography variant="body2" className="mb-2">
                          {message.content}
                        </Typography>
                        <Box display="flex" justifyContent="space-between">
                          <Typography variant="caption" color="textSecondary">
                            {t("communication.from")}: {message.sender_name}
                          </Typography>
                          <Typography variant="caption" color="textSecondary">
                            {new Date(message.created_at).toLocaleDateString("id-ID")}
                          </Typography>
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              ) : (
                <Typography variant="body2" color="textSecondary">
                  {t("communication.no-messages")}
                </Typography>
              )}
            </Box>
          )}

          {tabValue === 2 && (
            <Box className="mt-4">
              <Typography variant="body1">{t("communication.notifications-description")}</Typography>
              <Typography variant="body2" color="textSecondary" className="mt-2">
                {t("communication.coming-soon")}
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
}
