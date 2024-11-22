import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ShareIcon from '@mui/icons-material/Share';
import Modal from '@mui/material/Modal';
import TextField from '@mui/material/TextField';
import MenuItem from '@mui/material/MenuItem';
import IconButton from '@mui/material/IconButton';
import axios from 'axios';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemText from '@mui/material/ListItemText';
import DeleteIcon from '@mui/icons-material/Delete';
import PeopleIcon from '@mui/icons-material/People';

function DashBoard({ dashboard, deleteDashboard, onNavigate, permissionType, userEmail }) {
  const [shareModalOpen, setShareModalOpen] = useState(false);
  const [managePermissionsOpen, setManagePermissionsOpen] = useState(false);
  const [shareEmail, setShareEmail] = useState('');
  const [sharePermission, setSharePermission] = useState('view');
  const [currentPermissions, setCurrentPermissions] = useState([]);

  const viewDashboard = (e) => {
    e.stopPropagation();
    onNavigate('readOnlyDash', { dashboardId: dashboard.dashboard_id });
  };

  const editDashboard = (e) => {
    e.stopPropagation();
    onNavigate('singleDashboard', { dashboardId: dashboard.dashboard_id });
  };

  const handleDelete = (e) => {
    e.stopPropagation();
    if (deleteDashboard) {
      deleteDashboard(dashboard.dashboard_id);
    }
  };

  const handleShare = async () => {
    try {
      const requestBody = {
        dashboard_id: dashboard.dashboard_id,
        permissions: [
          {
            user_email: shareEmail,
            permission_type: sharePermission
          }
        ],
        requester_email: userEmail
      };

      const response = await axios.put(
        'http://localhost:8000/dashboards/permissions',
        requestBody  // Send the properly structured request body
      );
      
      if (response.data.status === 'success') {
        setShareModalOpen(false);
        setShareEmail('');
        setSharePermission('view');
        //alert('Dashboard shared successfully!');
      }
    } catch (error) {
      console.error('Error sharing dashboard:', error);
      alert('Failed to share dashboard. Please try again.');
    }
  };

  const fetchPermissions = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/dashboards/${dashboard.dashboard_id}/permissions?requester_email=${userEmail}`
      );
      setCurrentPermissions(response.data);
    } catch (error) {
      console.error('Error fetching permissions:', error);
      alert('Failed to fetch permissions');
    }
  };

  const handleDeletePermission = async (emailToDelete) => {
    try {
      await axios.delete('http://localhost:8000/dashboards/permissions', {
        data: {
          dashboard_id: dashboard.dashboard_id,
          user_email: emailToDelete,
          requester_email: userEmail
        }
      });
      
      fetchPermissions();
      alert('Permission deleted successfully');
    } catch (error) {
      console.error('Error deleting permission:', error);
      alert('Failed to delete permission');
    }
  };

  useEffect(() => {
    if (managePermissionsOpen) {
      fetchPermissions();
    }
  }, [managePermissionsOpen]);

  return (
    <Box 
      onClick={viewDashboard}
      className="dashboard-card"
      sx={{
        padding: 4,
        marginBottom: 3,
        backgroundColor: '#ffffff',
        cursor: 'pointer',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '250px',
        width: '300px',
        position: 'relative',
        transition: 'all 0.3s ease',
        '&:hover': {
          transform: 'translateY(-5px)',
          boxShadow: '0 8px 25px rgba(180,212,255,0.5)'
        }
      }}
    >
      {/* Share Button */}
      {(permissionType === 'owner' || permissionType === 'OWNER') && (
        <Box sx={{ position: 'absolute', top: 8, right: 8, display: 'flex', gap: 1 }}>
          <IconButton
            onClick={(e) => {
              e.stopPropagation();
              setShareModalOpen(true);
            }}
          >
            <ShareIcon />
          </IconButton>
          <IconButton
            onClick={(e) => {
              e.stopPropagation();
              setManagePermissionsOpen(true);
            }}
          >
            <PeopleIcon />
          </IconButton>
        </Box>
      )}

      {/* Icon Container */}
      <Box 
        sx={{ 
          backgroundColor: 'var(--pastel-primary)',
          borderRadius: '50%',
          padding: 2,
          marginBottom: 3,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          width: '80px',
          height: '80px',
          transition: 'all 0.3s ease',
          '&:hover': {
            backgroundColor: 'var(--pastel-secondary)'
          }
        }}
      >
        <DashboardIcon 
          sx={{ 
            fontSize: 40,
            color: 'var(--text-primary)'
          }} 
        />
      </Box>

      {/* Title */}
      <Typography 
        variant="h5" 
        sx={{ 
          mb: 3,
          color: 'var(--text-primary)',
          fontWeight: 600,
          textAlign: 'center',
          lineHeight: 1.3
        }}
      >
        {dashboard.dashboard_title}
      </Typography>

      {/* Action Buttons */}
      {deleteDashboard && (permissionType === 'owner' || permissionType === 'OWNER') && (
        <Box 
          sx={{ 
            display: 'flex', 
            gap: 2,
            justifyContent: 'center',
            width: '100%',
            marginTop: 'auto'
          }}
        >
          <Button 
            variant="contained" 
            className="custom-button"
            sx={{ 
              backgroundColor: 'var(--pastel-secondary)',
              color: 'var(--text-primary)',
              flex: 1,
              maxWidth: '120px',
              '&:hover': {
                backgroundColor: 'var(--pastel-accent)',
                color: '#ffffff'
              }
            }}
            onClick={editDashboard}
          >
            Edit
          </Button>

          <Button 
            variant="contained" 
            className="custom-button"
            sx={{ 
              backgroundColor: 'var(--pastel-danger)',
              color: 'var(--text-primary)',
              flex: 1,
              maxWidth: '120px',
              '&:hover': {
                backgroundColor: '#ff8080',
                color: '#ffffff'
              }
            }}
            onClick={handleDelete}
          >
            Delete
          </Button>
        </Box>

      )}
      {!deleteDashboard && permissionType === 'edit' && (
        <Box 
          sx={{ 
            display: 'flex', 
            gap: 2,
            justifyContent: 'center',
            width: '100%',
            marginTop: 'auto' // Push buttons to bottom
          }}
        >
          <Button 
            variant="contained" 
            className="custom-button"
            sx={{ 
              backgroundColor: 'var(--pastel-secondary)',
              color: 'var(--text-primary)',
              flex: 1,
              maxWidth: '120px',
              '&:hover': {
                backgroundColor: 'var(--pastel-accent)',
                color: '#ffffff'
              }
            }}
            onClick={editDashboard}
          >
            Edit
          </Button>
        </Box>
      )}

      {/* Share Modal */}
      <Modal
        open={shareModalOpen}
        onClose={() => setShareModalOpen(false)}
        onClick={(e) => e.stopPropagation()}
      >
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 400,
          bgcolor: 'background.paper',
          borderRadius: 2,
          boxShadow: 24,
          p: 4,
        }}>
          <Typography variant="h6" component="h2" sx={{ mb: 3 }}>
            Share Dashboard
          </Typography>
          
          <TextField
            fullWidth
            label="Email Address"
            value={shareEmail}
            onChange={(e) => setShareEmail(e.target.value)}
            sx={{ mb: 2 }}
          />
          
          <TextField
            fullWidth
            select
            label="Permission Type"
            value={sharePermission}
            onChange={(e) => setSharePermission(e.target.value)}
            sx={{ mb: 3 }}
          >
            <MenuItem value="view">View Only</MenuItem>
            <MenuItem value="edit">Can Edit</MenuItem>
          </TextField>
          
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
            <Button 
              variant="outlined" 
              onClick={(e) => {
                e.stopPropagation();
                setShareModalOpen(false);
              }}
            >
              Cancel
            </Button>
            <Button 
              variant="contained" 
              onClick={(e) => {
                e.stopPropagation();
                handleShare();
              }}
              disabled={!shareEmail}
            >
              Share
            </Button>
          </Box>
        </Box>
      </Modal>

      {/* Add new Manage Permissions Modal */}
      <Modal
        open={managePermissionsOpen}
        onClose={() => setManagePermissionsOpen(false)}
        onClick={(e) => e.stopPropagation()}
      >
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 400,
          bgcolor: 'background.paper',
          borderRadius: 2,
          boxShadow: 24,
          p: 4,
        }}>
          <Typography variant="h6" component="h2" sx={{ mb: 3 }}>
            Manage Permissions
          </Typography>
          
          {currentPermissions.length === 0 ? (
            <Typography color="text.secondary">
              No shared permissions
            </Typography>
          ) : (
            <List>
              {currentPermissions.map((permission) => (
                <ListItem
                  key={permission.user_email}
                  secondaryAction={
                    permission.permission_type !== 'owner' && (
                      <IconButton 
                        edge="end" 
                        aria-label="delete"
                        onClick={() => handleDeletePermission(permission.user_email)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    )
                  }
                >
                  <ListItemText
                    primary={permission.user_email}
                    secondary={`Permission: ${permission.permission_type}`}
                  />
                </ListItem>
              ))}
            </List>
          )}
          
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 3 }}>
            <Button 
              variant="contained" 
              onClick={(e) => {
                e.stopPropagation();
                setManagePermissionsOpen(false);
              }}
            >
              Close
            </Button>
          </Box>
        </Box>
      </Modal>
    </Box>
  );
}

export default DashBoard;
