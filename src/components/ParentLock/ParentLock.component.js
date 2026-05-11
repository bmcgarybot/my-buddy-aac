import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Dialog from '@material-ui/core/Dialog';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogContent from '@material-ui/core/DialogContent';
import DialogActions from '@material-ui/core/DialogActions';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import LockIcon from '@material-ui/icons/Lock';

import './ParentLock.css';

const DEFAULT_PIN = '1234';
const STORAGE_KEY = 'mybuddy_parent_pin';

class ParentLock extends Component {
  static propTypes = {
    open: PropTypes.bool.isRequired,
    onUnlock: PropTypes.func.isRequired,
    onCancel: PropTypes.func.isRequired
  };

  state = {
    pin: '',
    error: false,
    attempts: 0
  };

  getStoredPin() {
    try {
      return localStorage.getItem(STORAGE_KEY) || DEFAULT_PIN;
    } catch (e) {
      return DEFAULT_PIN;
    }
  }

  static setPin(newPin) {
    try {
      localStorage.setItem(STORAGE_KEY, newPin);
      return true;
    } catch (e) {
      return false;
    }
  }

  handlePinChange = (e) => {
    const val = e.target.value.replace(/\D/g, '').slice(0, 4);
    this.setState({ pin: val, error: false });

    if (val.length === 4) {
      setTimeout(() => this.checkPin(val), 100);
    }
  };

  checkPin = (pin) => {
    const storedPin = this.getStoredPin();
    if (pin === storedPin) {
      this.setState({ pin: '', error: false, attempts: 0 });
      this.props.onUnlock();
    } else {
      this.setState(prev => ({
        pin: '',
        error: true,
        attempts: prev.attempts + 1
      }));
    }
  };

  handleCancel = () => {
    this.setState({ pin: '', error: false });
    this.props.onCancel();
  };

  render() {
    const { open } = this.props;
    const { pin, error, attempts } = this.state;

    return (
      <Dialog
        open={open}
        onClose={this.handleCancel}
        className="ParentLock"
        maxWidth="xs"
        fullWidth
      >
        <DialogTitle className="ParentLock__title">
          <LockIcon className="ParentLock__icon" />
          <span>Parent Lock</span>
        </DialogTitle>
        <DialogContent className="ParentLock__content">
          <Typography variant="body2" gutterBottom>
            Enter your 4-digit PIN to access settings.
          </Typography>
          <TextField
            autoFocus
            type="password"
            inputProps={{
              maxLength: 4,
              pattern: '[0-9]*',
              inputMode: 'numeric',
              style: {
                fontSize: '2rem',
                textAlign: 'center',
                letterSpacing: '0.5em'
              }
            }}
            value={pin}
            onChange={this.handlePinChange}
            error={error}
            helperText={error ? `Incorrect PIN${attempts >= 3 ? ' (Default: 1234)' : ''}` : ' '}
            fullWidth
            variant="outlined"
            placeholder="● ● ● ●"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={this.handleCancel} color="default">
            Cancel
          </Button>
        </DialogActions>
      </Dialog>
    );
  }
}

export default ParentLock;
