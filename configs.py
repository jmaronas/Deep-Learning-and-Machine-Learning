from argparse import Namespace
from utils import squared_loss_function, grad_squared_loss_wrt_linear_model, absolute_loss_function, grad_absolute_loss_wrt_linear_model

loss_se_rl_11 = {
    'loss_y_lim_l' : -1,
    'loss_y_lim_u' : 6.3,
    'loss_x_lim_l' : -0.5,
    'loss_x_lim_u' : 2.5,
    'w_range_l' : -10,
    'w_range_u' : 10,
    'w_init' : 9,
    'w_range_l_2d' : -10,
    'w_range_u_2d' : 10,
    'b_range_l_2d' : -10,
    'b_range_u_2d' : 10,
    'w_init_full' : -5,
    'b_init_full' : -10,
    'total_loss_display_x' : 0,
    'total_loss_display_y' : 5,
    'total_loss_display_inc' : -0.25,
    'total_loss_display_loss_plot_inc' : 2.5,
    'per_point_loss_display_y_inc' : -0.5,
    'loss_name' : 'Squared Euclidean',
    'loss_fun' : squared_loss_function,
    'grad_loss_fun' : grad_squared_loss_wrt_linear_model,
    'gd_loss_fun_y_lim_u' : 400,
    'gd_loss_fun_y_lim_l' : -100,
    'gd_loss_fun_x_lim_u' : 12.5,
    'gd_loss_fun_x_lim_l' : -10.5,
    'gd_loss_fun_display_param_inc_y' : 1,
    'gd_loss_fun_display_param_y' : -50
}

loss_abs_rl_11 = {
    'loss_y_lim_l' : -1,
    'loss_y_lim_u' : 6.3,
    'loss_x_lim_l' : -0.5,
    'loss_x_lim_u' : 2.5,
    'w_range_l' : -3,
    'w_range_u' : 2,
    'w_init' : -2.5,
    'w_range_l_2d' : -10,
    'w_range_u_2d' : 10,
    'b_range_l_2d' : -9,
    'b_range_u_2d' : 9,
    'w_init_full' : -9,
    'b_init_full' : -3,
    'total_loss_display_x' : 0,
    'total_loss_display_y' : 5,
    'total_loss_display_inc' : -0.25,
    'total_loss_display_loss_plot_inc' : 0.5,
    'per_point_loss_display_y_inc' : -0.5,
    'loss_name' : 'Manhatan Distance',
    'loss_fun' : absolute_loss_function,
    'grad_loss_fun' : grad_absolute_loss_wrt_linear_model,
    'gd_loss_fun_y_lim_u' : 15,
    'gd_loss_fun_y_lim_l' : -2,
    'gd_loss_fun_x_lim_u' : 2.5,
    'gd_loss_fun_x_lim_l' : -3.5,
    'gd_loss_fun_display_param_inc_y' : -1,
    'gd_loss_fun_display_param_y' : 1
}


cg_rl_11 ={
    'seed':5,
    'N_domain_x' : 100,
    'N_models_simulation' : 100,
    'N_models_display' : 10,
    'data_x_name' : 'altura',
    'data_y_name' : 'peso',
    'data_y_lim_l' : 0,
    'data_y_lim_u' : 3.5,
    'data_x_lim_l' : -0.5,
    'data_x_lim_u' : 2.5,
    'data_y_lim_l_gd_pred_fun' : -10,
    'data_y_lim_u_gd_pred_fun' : 30,
    'data_x_range_l' : -1,
    'data_x_range_u' : 4,
    'fixed_bias' : 0.5,
    'y_axis_inc_text_data' : 0.1,
    'losses_named' : {'squared': Namespace(**loss_se_rl_11), 'absolute' : Namespace(**loss_abs_rl_11)},
    'losses' : [Namespace(**loss_se_rl_11),Namespace(**loss_abs_rl_11)]
}

cg_rl_11 = Namespace(**cg_rl_11)

