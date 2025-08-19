from argparse import Namespace
from utils import squared_loss_function, grad_squared_loss_wrt_linear_model, absolute_loss_function, grad_absolute_loss_wrt_linear_model
from utils import bce_loss_function, grad_bce_loss_wrt_sigmoid_model, brier_loss_function, grad_brier_loss_wrt_sigmoid_model

loss_se_rl_RR = {
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

loss_abs_rl_RR = {
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


cg_rl_RR ={
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
    'losses_named' : {'squared': Namespace(**loss_se_rl_RR), 'absolute' : Namespace(**loss_abs_rl_RR)},
    'losses' : [Namespace(**loss_se_rl_RR),Namespace(**loss_abs_rl_RR)]
}


loss_bce_rl_R01 = {
    'loss_y_lim_l' : -0.3,
    'loss_y_lim_u' : 1.3,
    'loss_x_lim_l' : -7,
    'loss_x_lim_u' : 7,
    'w_range_l' : -10,
    'w_range_u' : 10,
    'w_init' : -8,
    'w_range_l_2d' : -150,
    'w_range_u_2d' : 350,
    'b_range_l_2d' : -250,
    'b_range_u_2d' : 100,
    'w_init_full' : -50,
    'b_init_full' : -150,
    'total_loss_display_x' : 0,
    'total_loss_display_y' : 1.2,
    'total_loss_display_inc' : 0.05,
    'total_loss_display_loss_plot_inc' : 0.5,
    'per_point_loss_display_y_inc' : 0.05,
    'loss_name' : 'Binary Cross Entropy',
    'loss_fun' : bce_loss_function,
    'full_loss_display_azim' : -60,
    'grad_loss_fun' : grad_bce_loss_wrt_sigmoid_model,
    'gd_loss_fun_y_lim_u' : 120,
    'gd_loss_fun_y_lim_l' : -10.5,
    'gd_loss_fun_x_lim_u' : 10.5,
    'gd_loss_fun_x_lim_l' : -10.5,
    'gd_loss_fun_display_param_inc_y' : 1,
    'gd_loss_fun_display_param_y' : -1
}

loss_brier_rl_R01 = {
    'loss_y_lim_l' : -0.3,
    'loss_y_lim_u' : 1.3,
    'loss_x_lim_l' : -7,
    'loss_x_lim_u' : 7,
    'w_range_l' : -10,
    'w_range_u' : 10,
    'w_init' : -1.4,
    'w_range_l_2d' : -150,
    'w_range_u_2d' : 350,
    'b_range_l_2d' : -250,
    'b_range_u_2d' : 100,
    'w_init_full' : -0.5,
    'b_init_full' : -1,
    'total_loss_display_x' : 0,
    'total_loss_display_y' : 1.2,
    'total_loss_display_inc' : 0.05,
    'total_loss_display_loss_plot_inc' : 1,
    'per_point_loss_display_y_inc' : 0.05,
    'loss_name' : 'Brier Score',
    'loss_fun' : brier_loss_function,
    'full_loss_display_azim' : 20,
    'grad_loss_fun' : grad_brier_loss_wrt_sigmoid_model,
    'gd_loss_fun_y_lim_u' : 4,
    'gd_loss_fun_y_lim_l' : 0,
    'gd_loss_fun_x_lim_u' : 10,
    'gd_loss_fun_x_lim_l' : -10,
    'gd_loss_fun_display_param_inc_y' : -0.25,
    'gd_loss_fun_display_param_y' : 1
}


cg_rl_R01 ={
    'seed': 7, 
    'N_domain_x' : 100,
    'N_models_simulation' : 1000,
    'N_models_display' : 10,
    'data_x_name' : 'peso',
    'data_y_name' : 'probability of being dog',
    'data_y_lim_l' : -0.3,
    'data_y_lim_u' : 1.3,
    'data_x_lim_l' : -4,
    'data_x_lim_u' : 4,
    'data_y_lim_l_gd_pred_fun' : -0.5,
    'data_y_lim_u_gd_pred_fun' : 1.5,
    'data_x_range_l' : -7,
    'data_x_range_u' : 7,
    'fixed_bias' : 0.5,
    #'y_axis_inc_text_data' : 0.1,
    'losses_named' : {'bce' : Namespace(**loss_bce_rl_R01), 'brier': Namespace(**loss_brier_rl_R01) },
    'losses' : [Namespace(**loss_bce_rl_R01), Namespace(**loss_brier_rl_R01)]
}

loss_brier_rl_R201 = {
    #'loss_y_lim_l' : -0.3,
    'loss_y_lim_u' : 40,
    #'loss_x_lim_l' : -7,
    #'loss_x_lim_u' : 7,
    #'w_init_full' : -0.5,
    #'b_init_full' : -1,
    #'total_loss_display_x' : 0,
    #'total_loss_display_y' : 1.2,
    #'total_loss_display_inc' : 0.05,
    #'total_loss_display_loss_plot_inc' : 1,
    #'per_point_loss_display_y_inc' : 0.05,
    'loss_name' : 'Brier',
    'loss_fun' : brier_loss_function,
    'grad_loss_fun' : grad_brier_loss_wrt_sigmoid_model,
    #'gd_loss_fun_y_lim_u' : 4,
    #'gd_loss_fun_y_lim_l' : 0,
    #'gd_loss_fun_x_lim_u' : 10,
    #'gd_loss_fun_x_lim_l' : -10,
    #'gd_loss_fun_display_param_inc_y' : -0.25,
    #'gd_loss_fun_display_param_y' : 1
}

loss_bce_rl_R201 = {
    #'loss_y_lim_l' : -0.3,
    'loss_y_lim_u' : 20,
    #'loss_x_lim_l' : -7,
    #'loss_x_lim_u' : 7,
    #'w_init_full' : -0.5,
    #'b_init_full' : -1,
    #'total_loss_display_x' : 0,
    #'total_loss_display_y' : 1.2,
    #'total_loss_display_inc' : 0.05,
    #'total_loss_display_loss_plot_inc' : 1,
    #'per_point_loss_display_y_inc' : 0.05,
    'loss_name' : 'BCE',
    'loss_fun' : bce_loss_function,
    'grad_loss_fun' : grad_bce_loss_wrt_sigmoid_model,
    #'gd_loss_fun_y_lim_u' : 4,
    #'gd_loss_fun_y_lim_l' : 0,
    #'gd_loss_fun_x_lim_u' : 10,
    #'gd_loss_fun_x_lim_l' : -10,
    #'gd_loss_fun_display_param_inc_y' : -0.25,
    #'gd_loss_fun_display_param_y' : 1
}




cg_rl_R201 ={
    'seed': 1,
    'N_domain_x' : 100,
    'thr' : 0.5,
    #'N_models_simulation' : 1000,
    'N_models_display' : 20,
    'data_x1_name' : 'peso ($x_1$)',
    'data_x2_name' : 'altura ($x_2$)',
    'data_x1_lim_l' : -2,
    'data_x1_lim_u' : 7,
    'data_x2_lim_l' : -2,
    'data_x2_lim_u' : 7,
    'color_class0' : 'C0',
    'color_class1' : 'C1',
    'name_class0' : 'cat',
    'name_class1' : 'dog',
    #'data_y_lim_l_gd_pred_fun' : -0.5,
    #'data_y_lim_u_gd_pred_fun' : 1.5,
    #'data_x_range_l' : -7,
    #'data_x_range_u' : 7,
    #'fixed_bias' : 0.5,
    #'y_axis_inc_text_data' : 0.1,
    'losses_named' : {'bce' : Namespace(**loss_bce_rl_R01), 'brier': Namespace(**loss_brier_rl_R01) },
    'losses' : [Namespace(**loss_bce_rl_R201), Namespace(**loss_brier_rl_R201)]
}




cg_rl_R01 = Namespace(**cg_rl_R01)
cg_rl_R201 = Namespace(**cg_rl_R201)
cg_rl_RR = Namespace(**cg_rl_RR)

