classes = ['scratch']
num_classes = 1
model = dict(
    type='MaskRCNN',
    pretrained=None,
    backbone=dict(
        type='CBSwinTransformer',
        embed_dim=96,
        depths=[2, 2, 6, 2],
        num_heads=[3, 6, 12, 24],
        window_size=7,
        mlp_ratio=4.0,
        qkv_bias=True,
        qk_scale=None,
        drop_rate=0.0,
        attn_drop_rate=0.0,
        drop_path_rate=0.2,
        ape=False,
        patch_norm=True,
        out_indices=(0, 1, 2, 3),
        use_checkpoint=False),
    neck=dict(
        type='CBFPN',
        in_channels=[96, 192, 384, 768],
        out_channels=256,
        num_outs=5),
    rpn_head=dict(
        type='RPNHead',
        in_channels=256,
        feat_channels=256,
        anchor_generator=dict(
            type='AnchorGenerator',
            # scales=[8],

            scales = [1,1.15,1.3], #v13, v17
            base_sizes = [30,99,177,262,368],#v13, v17

            # scales = [1],#v14
            # base_sizes = [ 6.13915378, 15.30817663, 15.81447526, 38.35236013, 110.88941897],#v14

            # scales = [1, 1.1, 1.25], #v15
            # base_sizes = [99, 174, 240, 282, 339], #v15

            # scales = [224],#v11
            # ratios=[0.5, 1.0, 2.0],
            # ratios = [2.76267655, 2.61600145,  1.8355167, 3.04136575, 2.25080659], #v6
            # ratios = [0.88189713,1.88796302, 1.46820024, 3.46467267, 3.47708992], #v7 deleted
            # ratios = [1.57004273, 2.03738318, 1.87690971], #v7
            # ratios = [0.63692534, 0.49082569, 0.53279068], #v8
            # ratios = [2.45544554, 0.32258065, 1.28806584, 0.53349282, 0.84834123], #v10 - yolo anchor generator
            # ratios = [0.40740022,1.23485843,2.85315915,6.56536858,16.44087155], #v11
            # ratios = [0.3434203,0.94352366,1.92110634,3.7757587,7.58430032], #v12, v13 (clean data vs v11)
            # ratios = [0.26666587, 1.13321785, 0.4838764 , 0.65653432, 0.51883537], #v14 need to continue training if having time
            # ratios = [0.121, 0.232, 0.326, 0.51,  0.572, 0.654, 0.805, 0.843, 0.89,  1.108, 1.269, 1.403,2.276, 2.912, 5.667], #v15
            # ratios = [0.121, 0.326,  0.572, 0.805,  1.108, 1.403, 2.912, 5.667], #v15' eliminate some seemly redundant ratios
            ratios = [0.78317611,3.33879393,0.20926115,1.6726223,6.61393795,9.44650379,0.47774664,2.36350967,1.16334484,4.67465383], #v17
            
            strides=[4, 8, 16, 32, 64]), # keep intact because it totally depends on output of the backbone
            
            # strides = [3131.,4688.75,9507.375,11651.75,18884.5]),#v10
            # strides = [4.00446634,56.3339028,162.26243988,335.98506399,667.53152617]), #v11
            # strides = [3.9769167,55.70587774,159.89952107,327.70855591,628.87477123]),#v12
        # strides = [3.75250992, 23.87628289, 48.33591151, 14.08338183, 34.31873246]),
        # strides = [4, 24, 48, 14, 34]) #v6,
        # strides = [ 2, 8, 14, 24, 30]), #v7 deleted
        # strides = [1,3,10]), #v7
        bbox_coder=dict(
            type='DeltaXYWHBBoxCoder',
            target_means=[0.0, 0.0, 0.0, 0.0],
            target_stds=[1.0, 1.0, 1.0, 1.0]),
        loss_cls=dict(
            type='CrossEntropyLoss', use_sigmoid=True, loss_weight=1.0),
        loss_bbox=dict(type='L1Loss', loss_weight=1.0)),
    roi_head=dict(
        type='StandardRoIHead',
        bbox_roi_extractor=dict(
            type='SingleRoIExtractor',
            roi_layer=dict(type='RoIAlign', output_size=7, sampling_ratio=0),
            out_channels=256,
            featmap_strides=[4, 8, 16, 32]),
        bbox_head=dict(
            type='Shared2FCBBoxHead',
            in_channels=256,
            fc_out_channels=1024,
            roi_feat_size=7,
            num_classes=1,
            bbox_coder=dict(
                type='DeltaXYWHBBoxCoder',
                target_means=[0.0, 0.0, 0.0, 0.0],
                target_stds=[0.1, 0.1, 0.2, 0.2]),
            reg_class_agnostic=False,
            loss_cls=dict(
                type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0),
            loss_bbox=dict(type='L1Loss', loss_weight=1.0)),
        mask_roi_extractor=dict(
            type='SingleRoIExtractor',
            roi_layer=dict(type='RoIAlign', output_size=14, sampling_ratio=0),
            out_channels=256,
            featmap_strides=[4, 8, 16, 32]),
        mask_head=dict(
            type='FCNMaskHead',
            num_convs=4,
            in_channels=256,
            conv_out_channels=256,
            num_classes=1,
            loss_mask=dict(
                type='CrossEntropyLoss', use_mask=True, loss_weight=1.0))),
    train_cfg=dict(
        rpn=dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.7,
                neg_iou_thr=0.3,
                min_pos_iou=0.3,
                match_low_quality=True,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=256,
                pos_fraction=0.5,
                neg_pos_ub=-1,
                add_gt_as_proposals=False),
            allowed_border=-1,
            pos_weight=-1,
            debug=False),
        rpn_proposal=dict(
            nms_pre=2000,
            max_per_img=1000,
            nms=dict(type='nms', iou_threshold=0.7),
            min_bbox_size=0),
        rcnn=dict(
            assigner=dict(
                type='MaxIoUAssigner',
                pos_iou_thr=0.5,
                neg_iou_thr=0.5,
                min_pos_iou=0.5,
                match_low_quality=True,
                ignore_iof_thr=-1),
            sampler=dict(
                type='RandomSampler',
                num=512,
                pos_fraction=0.25,
                neg_pos_ub=-1,
                add_gt_as_proposals=True),
            mask_size=28,
            pos_weight=-1,
            debug=False)),
    test_cfg=dict(
        rpn=dict(
            nms_pre=1000,
            max_per_img=1000,
            nms=dict(type='nms', iou_threshold=0.7),
            min_bbox_size=0),
        rcnn=dict(
            score_thr=0.05,
            nms=dict(type='nms', iou_threshold=0.5),
            max_per_img=100,
            mask_thr_binary=0.5)))
dataset_type = 'CocoDataset'
data_root = 'data/scratch/'
img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
albu_train_transforms = [
    dict(
        type='OneOf',
        transforms=[
            dict(
                type='RGBShift',
                r_shift_limit=10,
                g_shift_limit=10,
                b_shift_limit=10,
                p=1.0),
            dict(
                type='HueSaturationValue',
                hue_shift_limit=20,
                sat_shift_limit=30,
                val_shift_limit=20,
                p=1.0)
        ],
        p=0.1)
]
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations', with_bbox=True, with_mask=True),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='Rotate', level=3, prob=0.1, max_rotate_angle=20),
    dict(
        type='Albu',
        transforms=[
            dict(
                type='OneOf',
                transforms=[
                    dict(
                        type='RGBShift',
                        r_shift_limit=10,
                        g_shift_limit=10,
                        b_shift_limit=10,
                        p=1.0),
                    dict(
                        type='HueSaturationValue',
                        hue_shift_limit=20,
                        sat_shift_limit=30,
                        val_shift_limit=20,
                        p=1.0)
                ],
                p=0.1)
        ],
        bbox_params=dict(
            type='BboxParams',
            format='pascal_voc',
            label_fields=['gt_labels'],
            min_visibility=0.0,
            filter_lost_elements=True),
        keymap=dict(img='image', gt_masks='masks', gt_bboxes='bboxes'),
        update_pad_shape=False,
        skip_img_without_anno=True),
    dict(
        type='AutoAugment',
        policies=[[{
            'type':
            'Resize',
            'img_scale': [(480, 1024), (512, 1024), (544, 1024), (576, 1024),
                          (608, 1024), (640, 1024), (672, 1024), (704, 1024),
                          (736, 1024), (768, 1024), (800, 1024)],
            'multiscale_mode':
            'value',
            'keep_ratio':
            True
        }],
                  [{
                      'type': 'Resize',
                      'img_scale': [(400, 1024), (500, 1024), (600, 1024)],
                      'multiscale_mode': 'value',
                      'keep_ratio': True
                  }, {
                      'type': 'RandomCrop',
                      'crop_type': 'absolute_range',
                      'crop_size': (384, 600),
                      'allow_negative_crop': True
                  }, {
                      'type':
                      'Resize',
                      'img_scale': [(480, 1024), (512, 1024), (544, 1024),
                                    (576, 1024), (608, 1024), (640, 1024),
                                    (672, 1024), (704, 1024), (736, 1024),
                                    (768, 1024), (800, 1024)],
                      'multiscale_mode':
                      'value',
                      'override':
                      True,
                      'keep_ratio':
                      True
                  }]]),
    dict(
        type='Normalize',
        mean=[123.675, 116.28, 103.53],
        std=[58.395, 57.12, 57.375],
        to_rgb=True),
    dict(type='Pad', size_divisor=32),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_bboxes', 'gt_labels', 'gt_masks'])
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1024, 800),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='Pad', size_divisor=32),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img'])
        ])
]
data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type='CocoDataset',
        classes=['scratch'],
        ann_file='data/scratch/annotations/clean_train_5k.json',
        img_prefix='data/scratch/images/',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='LoadAnnotations', with_bbox=True, with_mask=True),
            dict(type='RandomFlip', flip_ratio=0.5),
            dict(type='Rotate', level=3, prob=0.1, max_rotate_angle=20),
            dict(
                type='Albu',
                transforms=[
                    dict(
                        type='OneOf',
                        transforms=[
                            dict(
                                type='RGBShift',
                                r_shift_limit=10,
                                g_shift_limit=10,
                                b_shift_limit=10,
                                p=1.0),
                            dict(
                                type='HueSaturationValue',
                                hue_shift_limit=20,
                                sat_shift_limit=30,
                                val_shift_limit=20,
                                p=1.0)
                        ],
                        p=0.1)
                ],
                bbox_params=dict(
                    type='BboxParams',
                    format='pascal_voc',
                    label_fields=['gt_labels'],
                    min_visibility=0.0,
                    filter_lost_elements=True),
                keymap=dict(img='image', gt_masks='masks', gt_bboxes='bboxes'),
                update_pad_shape=False,
                skip_img_without_anno=True),
            dict(
                type='AutoAugment',
                policies=[[{
                    'type':
                    'Resize',
                    'img_scale': [(480, 1024), (512, 1024), (544, 1024),
                                  (576, 1024), (608, 1024), (640, 1024),
                                  (672, 1024), (704, 1024), (736, 1024),
                                  (768, 1024), (800, 1024)],
                    'multiscale_mode':
                    'value',
                    'keep_ratio':
                    True
                }],
                          [{
                              'type': 'Resize',
                              'img_scale': [(400, 1024), (500, 1024),
                                            (600, 1024)],
                              'multiscale_mode': 'value',
                              'keep_ratio': True
                          }, {
                              'type': 'RandomCrop',
                              'crop_type': 'absolute_range',
                              'crop_size': (384, 600),
                              'allow_negative_crop': True
                          }, {
                              'type':
                              'Resize',
                              'img_scale': [(480, 1024), (512, 1024),
                                            (544, 1024), (576, 1024),
                                            (608, 1024), (640, 1024),
                                            (672, 1024), (704, 1024),
                                            (736, 1024), (768, 1024),
                                            (800, 1024)],
                              'multiscale_mode':
                              'value',
                              'override':
                              True,
                              'keep_ratio':
                              True
                          }]]),
            dict(
                type='Normalize',
                mean=[123.675, 116.28, 103.53],
                std=[58.395, 57.12, 57.375],
                to_rgb=True),
            dict(type='Pad', size_divisor=32),
            dict(type='DefaultFormatBundle'),
            dict(
                type='Collect',
                keys=['img', 'gt_bboxes', 'gt_labels', 'gt_masks'])
        ]),
    val=dict(
        type='CocoDataset',
        classes=['scratch'],
        ann_file='data/scratch/annotations/clean_valid.json',
        img_prefix='data/scratch/images/',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(1024, 800),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=True),
                    dict(type='RandomFlip'),
                    dict(
                        type='Normalize',
                        mean=[123.675, 116.28, 103.53],
                        std=[58.395, 57.12, 57.375],
                        to_rgb=True),
                    dict(type='Pad', size_divisor=32),
                    dict(type='ImageToTensor', keys=['img']),
                    dict(type='Collect', keys=['img'])
                ])
        ]),
    test=dict(
        type='CocoDataset',
        classes=['scratch'],
        ann_file='data/scratch/annotations/test.json',
        img_prefix='data/scratch/images/',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(1024, 800),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=True),
                    dict(type='RandomFlip'),
                    dict(
                        type='Normalize',
                        mean=[123.675, 116.28, 103.53],
                        std=[58.395, 57.12, 57.375],
                        to_rgb=True),
                    dict(type='Pad', size_divisor=32),
                    dict(type='ImageToTensor', keys=['img']),
                    dict(type='Collect', keys=['img'])
                ])
        ]))
evaluation = dict(metric=['bbox', 'segm'])
optimizer = dict(
    type='AdamW',
    lr=0.0001,
    betas=(0.9, 0.999),
    weight_decay=0.05,
    paramwise_cfg=dict(
        custom_keys=dict(
            absolute_pos_embed=dict(decay_mult=0.0),
            relative_position_bias_table=dict(decay_mult=0.0),
            norm=dict(decay_mult=0.0))))
optimizer_config = dict(
    grad_clip=None,
    type='DistOptimizerHook',
    update_interval=1,
    coalesce=True,
    bucket_size_mb=-1,
    use_fp16=True)
lr_config = dict(
    policy='step',
    warmup='linear',
    warmup_iters=500,
    warmup_ratio=0.001,
    step=[22, 25])
runner = dict(type='EpochBasedRunnerAmp', max_epochs=30)
checkpoint_config = dict(interval=1)
log_config = dict(
    interval=50,
    hooks=[dict(type='TextLoggerHook'),
           dict(type='TensorboardLoggerHook')])
custom_hooks = [dict(type='NumClassCheckHook')]
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = '/mmdetection/checkpoints/scratch/pretrained_models/mask_rcnn_cbv2_swin_tiny_patch4_window7_mstrain_480-800_adamw_3x_coco.pth'
resume_from = '/mmdetection/checkpoints/scratch/demo_scratch_v17/latest.pth'
workflow = [('train', 1)]
fp16 = None
work_dir = '/mmdetection/checkpoints/scratch/demo_scratch_v17'
gpu_ids = range(0, 2)
