import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import {
  Alert,
  Box,
  Breadcrumbs,
  Button,
  Card,
  Chip,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  TextField,
  Typography,
} from "@mui/material";

import { DEFAULTS } from "@/config";
import NiStar from "@/icons/nexture/ni-star";

interface ParentPartnership {
  id: string;
  student_id: string;
  parent_id: string;
  partnership_type: string;
  relationship: string;
  contact_primary: string;
  contact_secondary: string;
  email: string;
  communication_preference: string;
  involvement_level: string;
  notes: string;
  is_active: boolean;
}

interface ParentCommunication {
  id: string;
  partnership_id: string;
  communication_type: string;
  communication_date: string;
  subject: string;
  content: string;
  direction: string;
  status: string;
}

interface ParentMeeting {
  id: string;
  partnership_id: string;
  meeting_type: string;
  scheduled_date: string;
  duration_minutes: number;
  status: string;
  attendance_status: string;
  location?: string;
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

export default function ParentPartnershipPage() {
  const { studentId } = useParams<{ studentId?: string }>();
  const [tabValue, setTabValue] = useState(0);
  const [partnerships, setPartnerships] = useState<ParentPartnership[]>([]);
  const [communications, setCommunications] = useState<ParentCommunication[]>([]);
  const [meetings, setMeetings] = useState<ParentMeeting[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openPartnershipDialog, setOpenPartnershipDialog] = useState(false);
  const [openCommunicationDialog, setOpenCommunicationDialog] = useState(false);
  const [openMeetingDialog, setOpenMeetingDialog] = useState(false);

  const [partnershipFormData, setPartnershipFormData] = useState({
    parent_id: "",
    partnership_type: "",
    relationship: "",
    contact_primary: "",
    contact_secondary: "",
    email: "",
    communication_preference: "PHONE",
    involvement_level: "MODERATE",
    notes: "",
  });

  const [communicationFormData, setCommunicationFormData] = useState({
    partnership_id: "",
    communication_type: "",
    subject: "",
    content: "",
    direction: "OUTGOING",
    status: "COMPLETED",
  });

  const [meetingFormData, setMeetingFormData] = useState({
    partnership_id: "",
    meeting_type: "",
    scheduled_date: "",
    duration_minutes: 30,
    location: "SCHOOL",
    agenda: "",
  });

  const fetchPartnerships = useCallback(async () => {
    setLoading(true);
    const token = localStorage.getItem("accessToken");
    try {
      const url = studentId
        ? `${DEFAULTS.API_URL}/api/v1/parent-partnership/student/${studentId}`
        : `${DEFAULTS.API_URL}/api/v1/parent-partnership`;
      const res = await fetch(url, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setPartnerships(json.data.partnerships || []);
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [studentId]);

  const fetchCommunications = useCallback(async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/parent-partnership/communications`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setCommunications(json.data.communications || []);
      }
    } catch (err: any) {
      setError(err.message);
    }
  }, []);

  const fetchMeetings = useCallback(async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/parent-partnership/meetings`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const json = await res.json();
      if (json.status === "success") {
        setMeetings(json.data.meetings || []);
      }
    } catch (err: any) {
      setError(err.message);
    }
  }, []);

  useEffect(() => {
    fetchPartnerships();
    fetchCommunications();
    fetchMeetings();
  }, [studentId, fetchPartnerships, fetchCommunications, fetchMeetings]);

  const handleCreatePartnership = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/parent-partnership`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...partnershipFormData,
          student_id: studentId,
        }),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenPartnershipDialog(false);
        fetchPartnerships();
        setPartnershipFormData({
          parent_id: "",
          partnership_type: "",
          relationship: "",
          contact_primary: "",
          contact_secondary: "",
          email: "",
          communication_preference: "PHONE",
          involvement_level: "MODERATE",
          notes: "",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleCreateCommunication = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/parent-partnership/communications`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(communicationFormData),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenCommunicationDialog(false);
        fetchCommunications();
        setCommunicationFormData({
          partnership_id: "",
          communication_type: "",
          subject: "",
          content: "",
          direction: "OUTGOING",
          status: "COMPLETED",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleCreateMeeting = async () => {
    const token = localStorage.getItem("accessToken");
    try {
      const res = await fetch(`${DEFAULTS.API_URL}/api/v1/parent-partnership/meetings`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(meetingFormData),
      });
      const json = await res.json();
      if (json.status === "success") {
        setOpenMeetingDialog(false);
        fetchMeetings();
        setMeetingFormData({
          partnership_id: "",
          meeting_type: "",
          scheduled_date: "",
          duration_minutes: 30,
          location: "SCHOOL",
          agenda: "",
        });
      } else {
        setError(json.message);
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  const getPartnershipTypeLabel = (type: string) => {
    switch (type) {
      case "PRIMARY":
        return "Utama";
      case "SECONDARY":
        return "Sekunder";
      case "EMERGENCY":
        return "Darurat";
      default:
        return type;
    }
  };

  const getRelationshipLabel = (relationship: string) => {
    switch (relationship) {
      case "FATHER":
        return "Ayah";
      case "MOTHER":
        return "Ibu";
      case "GUARDIAN":
        return "Wali";
      case "GRANDPARENT":
        return "Kakek/Nenek";
      default:
        return relationship;
    }
  };

  const getInvolvementColor = (level: string) => {
    switch (level) {
      case "LOW":
        return "error";
      case "MODERATE":
        return "info";
      case "HIGH":
        return "success";
      case "VERY_HIGH":
        return "primary";
      default:
        return "default";
    }
  };

  return (
    <Box>
      <Box className="mb-2 flex items-center justify-between">
        <Typography variant="h1" component="h1" className="mb-0">
          Kemitraan Orang Tua-Guru
        </Typography>
        <Button variant="contained" startIcon={<NiStar size="small" />} onClick={() => setOpenPartnershipDialog(true)}>
          Tambah Kemitraan
        </Button>
      </Box>
      <Breadcrumbs className="mb-6">
        <Link to="/home">Beranda</Link>
        {studentId ? (
          <>
            <Link to="/students">Siswa</Link>
            <Typography variant="body2">Kemitraan Orang Tua</Typography>
          </>
        ) : (
          <>
            <Link to="/academic">Akademik</Link>
            <Typography variant="body2">Kemitraan Orang Tua</Typography>
          </>
        )}
      </Breadcrumbs>

      <Alert severity="info" className="mb-6">
        Sistem tracking kolaborasi home-school untuk keberhasilan siswa SD.
      </Alert>

      {error && (
        <Alert severity="error" className="mb-4">
          {error}
        </Alert>
      )}

      <Box sx={{ borderBottom: 1, borderColor: "divider", mb: 3 }}>
        <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
          <Tab label="Kemitraan" />
          <Tab label="Komunikasi" />
          <Tab label="Pertemuan" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Tipe</TableCell>
                <TableCell className="font-bold">Hubungan</TableCell>
                <TableCell className="font-bold">Kontak Utama</TableCell>
                <TableCell className="font-bold">Email</TableCell>
                <TableCell className="font-bold">Preferensi</TableCell>
                <TableCell className="font-bold">Keterlibatan</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={6} align="center" className="py-10">
                    <CircularProgress size={24} />
                  </TableCell>
                </TableRow>
              ) : partnerships.length > 0 ? (
                partnerships.map((partnership) => (
                  <TableRow key={partnership.id} hover>
                    <TableCell>
                      <Chip label={getPartnershipTypeLabel(partnership.partnership_type)} size="small" />
                    </TableCell>
                    <TableCell>{getRelationshipLabel(partnership.relationship)}</TableCell>
                    <TableCell>{partnership.contact_primary}</TableCell>
                    <TableCell className="text-sm">{partnership.email}</TableCell>
                    <TableCell>{partnership.communication_preference}</TableCell>
                    <TableCell>
                      <Chip
                        label={partnership.involvement_level}
                        color={getInvolvementColor(partnership.involvement_level)}
                        size="small"
                      />
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={6} align="center" className="py-10">
                    Tidak ada data kemitraan orang tua.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Box className="mb-4">
          <Button
            variant="outlined"
            startIcon={<NiStar size="small" />}
            onClick={() => setOpenCommunicationDialog(true)}
          >
            Catat Komunikasi Baru
          </Button>
        </Box>
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Tipe</TableCell>
                <TableCell className="font-bold">Tanggal</TableCell>
                <TableCell className="font-bold">Subjek</TableCell>
                <TableCell className="font-bold">Arah</TableCell>
                <TableCell className="font-bold">Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {communications.length > 0 ? (
                communications.map((comm) => (
                  <TableRow key={comm.id} hover>
                    <TableCell>
                      <Chip label={comm.communication_type} size="small" />
                    </TableCell>
                    <TableCell className="text-sm">{comm.communication_date}</TableCell>
                    <TableCell>{comm.subject}</TableCell>
                    <TableCell>
                      <Chip
                        label={comm.direction}
                        color={comm.direction === "INCOMING" ? "success" : "info"}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip label={comm.status} size="small" />
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} align="center" className="py-10">
                    Tidak ada log komunikasi.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Box className="mb-4">
          <Button variant="outlined" startIcon={<NiStar size="small" />} onClick={() => setOpenMeetingDialog(true)}>
            Jadwalkan Pertemuan
          </Button>
        </Box>
        <TableContainer component={Card}>
          <Table>
            <TableHead>
              <TableRow className="bg-action-hover">
                <TableCell className="font-bold">Tipe Pertemuan</TableCell>
                <TableCell className="font-bold">Tanggal</TableCell>
                <TableCell className="font-bold">Durasi</TableCell>
                <TableCell className="font-bold">Lokasi</TableCell>
                <TableCell className="font-bold">Status</TableCell>
                <TableCell className="font-bold">Kehadiran</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {meetings.length > 0 ? (
                meetings.map((meeting) => (
                  <TableRow key={meeting.id} hover>
                    <TableCell>{meeting.meeting_type}</TableCell>
                    <TableCell className="text-sm">{meeting.scheduled_date}</TableCell>
                    <TableCell>{meeting.duration_minutes} menit</TableCell>
                    <TableCell>{meeting.location || "Sekolah"}</TableCell>
                    <TableCell>
                      <Chip label={meeting.status} size="small" />
                    </TableCell>
                    <TableCell>
                      <Chip label={meeting.attendance_status || "N/A"} size="small" />
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={6} align="center" className="py-10">
                    Tidak ada jadwal pertemuan.
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      {/* Partnership Dialog */}
      <Dialog open={openPartnershipDialog} onClose={() => setOpenPartnershipDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Tambah Kemitraan Orang Tua</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <TextField
              label="Parent ID"
              fullWidth
              value={partnershipFormData.parent_id}
              onChange={(e) => setPartnershipFormData({ ...partnershipFormData, parent_id: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Tipe Kemitraan</InputLabel>
              <Select
                value={partnershipFormData.partnership_type}
                label="Tipe Kemitraan"
                onChange={(e) => setPartnershipFormData({ ...partnershipFormData, partnership_type: e.target.value })}
              >
                <MenuItem value="PRIMARY">Utama</MenuItem>
                <MenuItem value="SECONDARY">Sekunder</MenuItem>
                <MenuItem value="EMERGENCY">Darurat</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Hubungan</InputLabel>
              <Select
                value={partnershipFormData.relationship}
                label="Hubungan"
                onChange={(e) => setPartnershipFormData({ ...partnershipFormData, relationship: e.target.value })}
              >
                <MenuItem value="FATHER">Ayah</MenuItem>
                <MenuItem value="MOTHER">Ibu</MenuItem>
                <MenuItem value="GUARDIAN">Wali</MenuItem>
                <MenuItem value="GRANDPARENT">Kakek/Nenek</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Kontak Utama"
              fullWidth
              value={partnershipFormData.contact_primary}
              onChange={(e) => setPartnershipFormData({ ...partnershipFormData, contact_primary: e.target.value })}
            />
            <TextField
              label="Kontak Sekunder"
              fullWidth
              value={partnershipFormData.contact_secondary}
              onChange={(e) => setPartnershipFormData({ ...partnershipFormData, contact_secondary: e.target.value })}
            />
            <TextField
              label="Email"
              fullWidth
              type="email"
              value={partnershipFormData.email}
              onChange={(e) => setPartnershipFormData({ ...partnershipFormData, email: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Preferensi Komunikasi</InputLabel>
              <Select
                value={partnershipFormData.communication_preference}
                label="Preferensi Komunikasi"
                onChange={(e) =>
                  setPartnershipFormData({ ...partnershipFormData, communication_preference: e.target.value })
                }
              >
                <MenuItem value="PHONE">Telepon</MenuItem>
                <MenuItem value="EMAIL">Email</MenuItem>
                <MenuItem value="WHATSAPP">WhatsApp</MenuItem>
                <MenuItem value="IN_PERSON">Tatap Muka</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Tingkat Keterlibatan</InputLabel>
              <Select
                value={partnershipFormData.involvement_level}
                label="Tingkat Keterlibatan"
                onChange={(e) => setPartnershipFormData({ ...partnershipFormData, involvement_level: e.target.value })}
              >
                <MenuItem value="LOW">Rendah</MenuItem>
                <MenuItem value="MODERATE">Sedang</MenuItem>
                <MenuItem value="HIGH">Tinggi</MenuItem>
                <MenuItem value="VERY_HIGH">Sangat Tinggi</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Catatan"
              fullWidth
              multiline
              rows={2}
              value={partnershipFormData.notes}
              onChange={(e) => setPartnershipFormData({ ...partnershipFormData, notes: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenPartnershipDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreatePartnership}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>

      {/* Communication Dialog */}
      <Dialog open={openCommunicationDialog} onClose={() => setOpenCommunicationDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Catat Komunikasi Baru</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <TextField
              label="Partnership ID"
              fullWidth
              value={communicationFormData.partnership_id}
              onChange={(e) => setCommunicationFormData({ ...communicationFormData, partnership_id: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Tipe Komunikasi</InputLabel>
              <Select
                value={communicationFormData.communication_type}
                label="Tipe Komunikasi"
                onChange={(e) =>
                  setCommunicationFormData({ ...communicationFormData, communication_type: e.target.value })
                }
              >
                <MenuItem value="PHONE_CALL">Telepon</MenuItem>
                <MenuItem value="EMAIL">Email</MenuItem>
                <MenuItem value="MEETING">Pertemuan</MenuItem>
                <MenuItem value="WHATSAPP">WhatsApp</MenuItem>
                <MenuItem value="NOTE">Catatan</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Subjek"
              fullWidth
              value={communicationFormData.subject}
              onChange={(e) => setCommunicationFormData({ ...communicationFormData, subject: e.target.value })}
            />
            <TextField
              label="Isi Komunikasi"
              fullWidth
              multiline
              rows={3}
              value={communicationFormData.content}
              onChange={(e) => setCommunicationFormData({ ...communicationFormData, content: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Arah</InputLabel>
              <Select
                value={communicationFormData.direction}
                label="Arah"
                onChange={(e) => setCommunicationFormData({ ...communicationFormData, direction: e.target.value })}
              >
                <MenuItem value="INCOMING">Masuk</MenuItem>
                <MenuItem value="OUTGOING">Keluar</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Status</InputLabel>
              <Select
                value={communicationFormData.status}
                label="Status"
                onChange={(e) => setCommunicationFormData({ ...communicationFormData, status: e.target.value })}
              >
                <MenuItem value="SCHEDULED">Terjadwal</MenuItem>
                <MenuItem value="COMPLETED">Selesai</MenuItem>
                <MenuItem value="CANCELLED">Dibatalkan</MenuItem>
                <MenuItem value="FOLLOW_UP">Follow-up</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenCommunicationDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreateCommunication}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>

      {/* Meeting Dialog */}
      <Dialog open={openMeetingDialog} onClose={() => setOpenMeetingDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Jadwalkan Pertemuan</DialogTitle>
        <DialogContent>
          <Box className="grid gap-4 pt-4">
            <TextField
              label="Partnership ID"
              fullWidth
              value={meetingFormData.partnership_id}
              onChange={(e) => setMeetingFormData({ ...meetingFormData, partnership_id: e.target.value })}
            />
            <FormControl fullWidth>
              <InputLabel>Tipe Pertemuan</InputLabel>
              <Select
                value={meetingFormData.meeting_type}
                label="Tipe Pertemuan"
                onChange={(e) => setMeetingFormData({ ...meetingFormData, meeting_type: e.target.value })}
              >
                <MenuItem value="PARENT_TEACHER_CONFERENCE">Konferensi Guru-Orang Tua</MenuItem>
                <MenuItem value="IEP_MEETING">Rapat IEP</MenuItem>
                <MenuItem value="BEHAVIOR_DISCUSSION">Diskusi Perilaku</MenuItem>
                <MenuItem value="ACADEMIC_REVIEW">Review Akademik</MenuItem>
              </Select>
            </FormControl>
            <TextField
              label="Tanggal Pertemuan"
              type="datetime-local"
              fullWidth
              InputLabelProps={{ shrink: true }}
              value={meetingFormData.scheduled_date}
              onChange={(e) => setMeetingFormData({ ...meetingFormData, scheduled_date: e.target.value })}
            />
            <TextField
              label="Durasi (menit)"
              type="number"
              fullWidth
              value={meetingFormData.duration_minutes}
              onChange={(e) => setMeetingFormData({ ...meetingFormData, duration_minutes: parseInt(e.target.value) })}
            />
            <TextField
              label="Lokasi"
              fullWidth
              value={meetingFormData.location}
              onChange={(e) => setMeetingFormData({ ...meetingFormData, location: e.target.value })}
            />
            <TextField
              label="Agenda"
              fullWidth
              multiline
              rows={3}
              value={meetingFormData.agenda}
              onChange={(e) => setMeetingFormData({ ...meetingFormData, agenda: e.target.value })}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenMeetingDialog(false)}>Batal</Button>
          <Button variant="contained" onClick={handleCreateMeeting}>
            Simpan
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}
