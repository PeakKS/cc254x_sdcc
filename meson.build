project (
  'cc2540',
)

flags = [
  '-mmcs51',
  '--model-medium',
  '--xram-loc 0x0000',
  '--xram-size 0x2000',
  '--iram-size 0x0100',
  '-DUART0',
  '-Wa,-glos',
  '-Wa,-p'
]

common_lib = static_library (
  'common',
  sources: [
    'delay.c',
    'time.c',
    'uart.c',
    'usb.c',
    'usb_cdc_acm.c',
    'util.c',
  ],
  c_args: flags,
)

common_dep = declare_dependency (
  link_with: [
    common_lib,
  ],
  include_directories: '/usr/share/sdcc/include',
)

executable(
  'blink',
  sources: [
    'test_blink.c',
  ],
  c_args: flags,
  dependencies: [
    common_dep,
  ]
)