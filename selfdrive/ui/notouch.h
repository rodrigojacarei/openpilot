#pragma once

#include <QVBoxLayout>
#include <QWidget>

#include "selfdrive/ui/qt/onroad.h"
#include "selfdrive/ui/qt/offroad/settings.h"
#include "tools/replay/replay.h"

class MainWindowNoTouch : public QWidget {
  Q_OBJECT

public:
  explicit MainWindowNoTouch(QWidget *parent = 0);

private:
  QVBoxLayout *main_layout;

  OnroadWindow *onroad;
  std::unique_ptr<Replay> replay;
};
