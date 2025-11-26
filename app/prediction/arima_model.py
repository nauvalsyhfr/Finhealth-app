"""
FinHealth ARIMA Forecasting Module
Time series forecasting for UMKM financial data
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import warnings
warnings.filterwarnings('ignore')


class FinancialForecaster:
    """
    ARIMA-based financial forecasting system
    Predicts future income, expenses, and cashflow
    """
    
    def __init__(self):
        self.models = {}
        self.forecasts = {}
        self.best_orders = {}
    
    def load_data(self, df, date_col='Hari/Tanggal'):
        """
        Load and prepare time series data
        
        Args:
            df (DataFrame): Input data with financial metrics
            date_col (str): Name of date column
        
        Returns:
            DataFrame: Cleaned and prepared data
        """
        # Make a copy
        data = df.copy()
        
        # Convert date column
        if date_col in data.columns:
            data[date_col] = pd.to_datetime(data[date_col], errors='coerce')
            data = data.sort_values(date_col)
            data.set_index(date_col, inplace=True)
        
        # Remove any rows with missing dates
        data = data[data.index.notna()]
        
        # Handle missing values
        numeric_cols = ['Pemasukan', 'Pengeluaran', 'Cashflow', 'Jumlah Transaksi']
        for col in numeric_cols:
            if col in data.columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')
                data[col].fillna(data[col].median(), inplace=True)
        
        return data
    
    def find_best_arima_order(self, series, max_p=3, max_d=2, max_q=3):
        """
        Find best ARIMA order using AIC
        
        Args:
            series: Time series data
            max_p, max_d, max_q: Maximum values for ARIMA(p,d,q)
        
        Returns:
            tuple: Best (p, d, q) order
        """
        best_aic = np.inf
        best_order = (1, 1, 1)
        
        # Check for stationarity
        try:
            adf_result = adfuller(series.dropna())
            d = 0 if adf_result[1] < 0.05 else 1
        except:
            d = 1
        
        # Grid search for best parameters
        for p in range(0, max_p + 1):
            for q in range(0, max_q + 1):
                try:
                    model = ARIMA(series, order=(p, d, q))
                    fitted = model.fit()
                    
                    if fitted.aic < best_aic:
                        best_aic = fitted.aic
                        best_order = (p, d, q)
                except:
                    continue
        
        return best_order
    
    def fit_model(self, data, target_col, order=None):
        """
        Fit ARIMA model to a specific column
        
        Args:
            data (DataFrame): Time series data
            target_col (str): Column to forecast
            order (tuple): ARIMA order (p,d,q) or None for auto
        
        Returns:
            dict: Model info and metrics
        """
        if target_col not in data.columns:
            raise ValueError(f"Column {target_col} not found in data")
        
        series = data[target_col].dropna()
        
        if len(series) < 10:
            raise ValueError(f"Insufficient data points for {target_col}. Need at least 10.")
        
        # Find best order if not provided
        if order is None:
            order = self.find_best_arima_order(series)
        
        # Fit model
        try:
            model = ARIMA(series, order=order)
            fitted_model = model.fit()
            
            self.models[target_col] = fitted_model
            self.best_orders[target_col] = order
            
            return {
                'success': True,
                'order': order,
                'aic': fitted_model.aic,
                'bic': fitted_model.bic,
                'data_points': len(series)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def forecast(self, target_col, steps=6, alpha=0.05):
        """
        Generate forecast for specified periods
        
        Args:
            target_col (str): Column to forecast
            steps (int): Number of periods ahead
            alpha (float): Significance level for confidence intervals
        
        Returns:
            dict: Forecast values and confidence intervals
        """
        if target_col not in self.models:
            raise ValueError(f"Model for {target_col} not fitted yet")
        
        model = self.models[target_col]
        
        # Generate forecast
        forecast_result = model.forecast(steps=steps, alpha=alpha)
        conf_int = model.get_forecast(steps=steps).conf_int(alpha=alpha)
        
        # Store results
        self.forecasts[target_col] = {
            'values': forecast_result.tolist(),
            'lower_bound': conf_int.iloc[:, 0].tolist(),
            'upper_bound': conf_int.iloc[:, 1].tolist()
        }
        
        return self.forecasts[target_col]
    
    def predict_all(self, df, forecast_months=6):
        """
        Complete prediction pipeline for all metrics
        
        Args:
            df (DataFrame): Input financial data
            forecast_months (int): Number of months to forecast
        
        Returns:
            dict: Complete forecast results with metadata
        """
        try:
            # Load and prepare data
            data = self.load_data(df)
            
            if len(data) < 10:
                return {
                    'success': False,
                    'error': 'Data tidak cukup. Minimal 10 data point diperlukan.'
                }
            
            # Columns to forecast
            forecast_cols = {
                'Pemasukan': 'pemasukan',
                'Pengeluaran': 'pengeluaran',
                'Cashflow': 'cashflow',
                'Jumlah Transaksi': 'transaksi'
            }
            
            results = {
                'success': True,
                'data_summary': {
                    'start_date': data.index.min().strftime('%Y-%m-%d'),
                    'end_date': data.index.max().strftime('%Y-%m-%d'),
                    'total_records': len(data)
                },
                'models': {},
                'forecasts': []
            }
            
            # Fit models and generate forecasts
            last_date = data.index.max()
            
            for col, key in forecast_cols.items():
                if col in data.columns:
                    # Fit model
                    model_info = self.fit_model(data, col)
                    
                    if model_info['success']:
                        # Generate forecast
                        forecast_data = self.forecast(col, steps=forecast_months)
                        
                        results['models'][key] = {
                            'order': str(model_info['order']),
                            'aic': round(model_info['aic'], 2),
                            'bic': round(model_info['bic'], 2)
                        }
                        
                        # Store forecast by month
                        for i in range(forecast_months):
                            forecast_date = last_date + timedelta(days=30 * (i + 1))
                            
                            if i >= len(results['forecasts']):
                                results['forecasts'].append({
                                    'forecast_month': i + 1,
                                    'forecast_date': forecast_date.strftime('%Y-%m-%d')
                                })
                            
                            results['forecasts'][i][f'predicted_{key}'] = round(forecast_data['values'][i], 2)
                            results['forecasts'][i][f'{key}_lower'] = round(forecast_data['lower_bound'][i], 2)
                            results['forecasts'][i][f'{key}_upper'] = round(forecast_data['upper_bound'][i], 2)
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error dalam prediksi: {str(e)}'
            }
    
    def validate_csv_format(self, df):
        """
        Validate uploaded CSV format
        
        Args:
            df (DataFrame): Uploaded data
        
        Returns:
            dict: Validation result
        """
        required_cols = ['Hari/Tanggal', 'Pemasukan', 'Pengeluaran', 'Jumlah Transaksi', 'Cashflow']
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            return {
                'valid': False,
                'error': f'Kolom yang hilang: {", ".join(missing_cols)}',
                'required_columns': required_cols
            }
        
        # Check for minimum rows
        if len(df) < 10:
            return {
                'valid': False,
                'error': 'Data terlalu sedikit. Minimal 10 baris data diperlukan.',
                'row_count': len(df)
            }
        
        return {
            'valid': True,
            'row_count': len(df),
            'columns': list(df.columns)
        }


def forecast_financial_data(df, forecast_months=6):
    """
    Wrapper function for API integration
    
    Args:
        df (DataFrame): Input financial data
        forecast_months (int): Forecast period
    
    Returns:
        dict: Complete forecast results
    """
    forecaster = FinancialForecaster()
    return forecaster.predict_all(df, forecast_months)